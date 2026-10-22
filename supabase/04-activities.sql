-- PyQuest: vocabulário, oficina e explicações. Execute após a carga 02-questions.sql.
-- Novas questões usam IDs próprios; partidas antigas mantêm seus conteúdos.
begin;
alter table public.pq_rooms add column if not exists reflections_enabled boolean not null default false;
alter table public.pq_rooms add column if not exists activity_pack text not null default 'quiz';
alter table public.pq_rooms drop constraint if exists pq_rooms_status_check;
alter table public.pq_rooms add constraint pq_rooms_status_check check(status in('lobby','active','reflection','reveal','finished'));
create table if not exists public.pq_reflections(
 room uuid not null,user_id uuid not null,question int not null,
 text text not null check(char_length(trim(text)) between 8 and 400),
 created_at timestamptz not null default clock_timestamp(),
 primary key(room,user_id,question),foreign key(room,user_id) references public.pq_players(room,user_id)
);
alter table public.pq_reflections enable row level security;
revoke all on public.pq_reflections from public,anon,authenticated;

create or replace function public.pq_create_activity_room(p_title text,p_count int,p_seconds int,p_pack text,p_reflections boolean) returns uuid language plpgsql security definer set search_path='' as $$
declare rid uuid;qids int[];invite text;available int;
begin
 perform public.pq_teacher_check();
 if p_title is null or length(trim(p_title)) not between 1 and 60 or p_count is null or p_count<1 or p_seconds is null or p_seconds not in(0,30,60,90,120,180) or p_pack is null or p_pack not in('mixed','quiz','classify','repair','reflect') then raise exception 'Configuração inválida.'; end if;
 select count(*) into available from public.pq_questions where data->>'curriculum'='poo-v3'
 and (p_pack='mixed' or data->>'activity'=p_pack or (p_pack='reflect' and data->>'activity'='quiz' and coalesce(data->>'reflection_prompt','')<>''));
 if available=0 or p_count>available or (p_count not in(5,10,15) and p_count<>available) then raise exception 'Quantidade inválida para esta atividade.'; end if;
 select array_agg(id order by pos) into qids from(select id,(data->>'position')::int pos from public.pq_questions where data->>'curriculum'='poo-v3'
 and (p_pack='mixed' or data->>'activity'=p_pack or (p_pack='reflect' and data->>'activity'='quiz' and coalesce(data->>'reflection_prompt','')<>'')) order by (data->>'position')::int limit p_count) q;
 loop
 invite:=upper(substr(replace(gen_random_uuid()::text,'-',''),1,6));
 begin
 insert into public.pq_rooms(host,title,code,question_ids,seconds,reflections_enabled,activity_pack)
 values(auth.uid(),trim(p_title),invite,qids,p_seconds,p_pack='reflect' or coalesce(p_reflections,true),p_pack) returning id into rid;
 exit;
 exception when unique_violation then null;
 end;
 end loop;
 return rid;
end $$;

-- Mantém o contrato de clientes anteriores, sem abrir etapa de escrita neles.
create or replace function public.pq_create_room(p_title text,p_count int,p_seconds int) returns uuid language plpgsql security definer set search_path='' as $$
begin
 return public.pq_create_activity_room(p_title,p_count,p_seconds,'quiz',false);
end $$;

create or replace function public.pq_advance(p_room uuid,p_expected text,p_current int) returns void language plpgsql security definer set search_path='' as $$
declare r public.pq_rooms; q jsonb;
begin
 select * into r from public.pq_rooms where id=p_room for update;
 if r.host is distinct from auth.uid() or auth.uid() is null then raise exception 'Apenas o professor pode controlar a partida.'; end if;
 if r.status<>p_expected or r.current<>p_current then raise exception 'A sala já avançou. Aguarde a atualização.'; end if;
 if r.status='lobby' and not exists(select 1 from public.pq_players where room=r.id) then raise exception 'Aguarde pelo menos um participante.'; end if;
 if r.status in('lobby','reveal') then
   if r.current+1>=array_length(r.question_ids,1) then update public.pq_rooms set status='finished' where id=r.id;
   else update public.pq_rooms set status='active',current=current+1,started_at=clock_timestamp() where id=r.id; end if;
 elsif r.status='active' then
   select data into q from public.pq_questions where id=r.question_ids[r.current+1];
   update public.pq_rooms set status=case when r.reflections_enabled and coalesce(q->>'reflection_prompt','')<>'' then 'reflection' else 'reveal' end where id=r.id;
 elsif r.status='reflection' then update public.pq_rooms set status='reveal' where id=r.id;
 end if;
end $$;

create or replace function public.pq_reflect(p_room uuid,p_question int,p_text text) returns void language plpgsql security definer set search_path='' as $$
declare r public.pq_rooms;q jsonb;
begin
 select * into r from public.pq_rooms where id=p_room for update;
 if auth.uid() is null or not exists(select 1 from public.pq_players where room=p_room and user_id=auth.uid()) then raise exception 'Você não participa desta sala.'; end if;
 select data into q from public.pq_questions where id=r.question_ids[r.current+1];
 if r.status<>'reflection' or r.current<>p_question or not r.reflections_enabled or coalesce(q->>'reflection_prompt','')='' then raise exception 'A etapa de explicação não está aberta.'; end if;
 if p_text is null or char_length(trim(p_text)) not between 8 and 400 then raise exception 'Escreva uma explicação de 8 a 400 caracteres.'; end if;
 insert into public.pq_reflections(room,user_id,question,text) values(p_room,auth.uid(),p_question,trim(p_text))
 on conflict(room,user_id,question) do update set text=excluded.text;
end $$;

create or replace function public.pq_state(p_room uuid) returns jsonb language plpgsql security definer set search_path='' as $$
declare r public.pq_rooms;q jsonb;players jsonb;mine jsonb;dist jsonb;answered int;is_host boolean;my_text text;reflections jsonb;reflection_count int;
begin
 select * into r from public.pq_rooms where id=p_room;
 is_host:=r.host=auth.uid();
 if r.id is null or auth.uid() is null or (not is_host and not exists(select 1 from public.pq_players where room=p_room and user_id=auth.uid())) then raise exception 'Sem acesso a esta sala.'; end if;
 select coalesce(jsonb_agg(to_jsonb(p) order by p.points desc,p.correct desc,p.elapsed,p.name),'[]') into players from (
 select p.name,p.avatar,coalesce(sum(a.points),0) points,count(*) filter(where a.correct) correct,
 coalesce(sum(a.elapsed) filter(where a.correct),0) elapsed
 from public.pq_players p left join public.pq_answers a on a.room=p.room and a.user_id=p.user_id and (r.status in('reveal','finished') or a.question<r.current)
 where p.room=p_room group by p.user_id,p.name,p.avatar) p;
 select count(*) into answered from public.pq_answers where room=p_room and question=r.current;
 if r.current>=0 then
 select data into q from public.pq_questions where id=r.question_ids[r.current+1];
 if r.status in('active','reflection') then q:=q-'answer'-'explanation'-'repair_variants'-'repair_original_output'; end if;
 if not r.reflections_enabled then q:=q-'reflection_prompt'; end if;
 end if;
 select jsonb_build_object('choice',a.choice,'points',case when r.status in('active','reflection') then null else a.points end) into mine from public.pq_answers a where room=p_room and user_id=auth.uid() and question=r.current;
 select text into my_text from public.pq_reflections where room=p_room and user_id=auth.uid() and question=r.current;
 select count(*) into reflection_count from public.pq_reflections where room=p_room and question=r.current;
 if is_host and r.status in('reflection','reveal','finished') then
 select coalesce(jsonb_agg(jsonb_build_object('name',p.name,'avatar',p.avatar,'text',f.text) order by p.name),'[]') into reflections from public.pq_players p left join public.pq_reflections f on f.room=p.room and f.user_id=p.user_id and f.question=r.current where p.room=p_room;
 end if;
 if is_host and r.status='reveal' then
 select jsonb_agg(n order by i) into dist from(select i,(select count(*) from public.pq_answers where room=p_room and question=r.current and choice=i) n from generate_series(0,3) i) d;
 end if;
 return jsonb_build_object('id',r.id,'title',r.title,'code',r.code,'status',r.status,'current',r.current,'total',array_length(r.question_ids,1),'started_at',r.started_at,'server_now',clock_timestamp(),'duration',case when r.seconds=0 then (q->>'seconds')::int else r.seconds end,'question',q,'is_host',is_host,'players',players,'my_answer',mine,'answered',answered,'distribution',dist,'my_reflection',my_text,'reflections',reflections,'reflection_count',reflection_count,'reflections_enabled',r.reflections_enabled,'activity_pack',r.activity_pack);
end $$;

create or replace function public.pq_export(p_room uuid) returns jsonb language plpgsql security definer set search_path='' as $$
declare r public.pq_rooms;result jsonb;
begin
 select * into r from public.pq_rooms where id=p_room;
 if r.host is distinct from auth.uid() or auth.uid() is null then raise exception 'Apenas o professor pode exportar.'; end if;
 select coalesce(jsonb_agg(jsonb_build_object('Aluno',p.name,'Sala',r.code,'Questao',q.data->>'title','Conceito',q.data->>'concept','Tipo',coalesce(q.data->>'kind','Quiz'),'Resposta',coalesce(q.data->'options'->>a.choice,'Sem resposta'),'Correta',q.data->'options'->>(q.data->>'answer')::int,'Acertou',case when a.correct then 'Sim' else 'Não' end,'Tempo_s',a.elapsed,'Pontos',coalesce(a.points,0),'Pergunta_explicacao',case when r.reflections_enabled then coalesce(q.data->>'reflection_prompt','') else '' end,'Justificativa',coalesce(f.text,'')) order by p.name,seq.i),'[]') into result
 from public.pq_players p cross join unnest(r.question_ids) with ordinality seq(qid,i)
 join public.pq_questions q on q.id=seq.qid
 left join public.pq_answers a on a.room=p.room and a.user_id=p.user_id and a.question=seq.i-1
 left join public.pq_reflections f on f.room=p.room and f.user_id=p.user_id and f.question=seq.i-1
 where p.room=p_room;
 return result;
end $$;
revoke all on function public.pq_create_activity_room(text,int,int,text,boolean), public.pq_reflect(uuid,int,text) from public,anon,authenticated;
grant execute on function public.pq_create_activity_room(text,int,int,text,boolean), public.pq_reflect(uuid,int,text) to authenticated;
commit;
