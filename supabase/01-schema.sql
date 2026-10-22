-- PyQuest — Mauricésar Barbosa. Execute em um projeto Supabase novo.
begin;
create table public.pq_teachers(user_id uuid primary key references auth.users(id));
create table public.pq_questions(id int primary key, data jsonb not null);
create table public.pq_rooms(
 id uuid primary key default gen_random_uuid(),host uuid not null references auth.users(id),
 title text not null,code text unique not null,status text not null default 'lobby' check(status in('lobby','active','reveal','finished')),
 current int not null default -1,question_ids int[] not null,seconds int not null default 0,
 started_at timestamptz,created_at timestamptz not null default now()
);
create table public.pq_players(
 room uuid references public.pq_rooms(id),user_id uuid references auth.users(id),
 name text not null check(length(name) between 2 and 24),avatar text not null,
 primary key(room,user_id),unique(room,name)
);
create table public.pq_answers(
 room uuid not null, user_id uuid not null, question int not null,choice int not null check(choice between 0 and 3),
 elapsed numeric not null,correct boolean not null,points int not null,created_at timestamptz not null default clock_timestamp(),
 primary key(room,user_id,question),foreign key(room,user_id) references public.pq_players(room,user_id)
);
alter table public.pq_teachers enable row level security;
alter table public.pq_questions enable row level security;
alter table public.pq_rooms enable row level security;
alter table public.pq_players enable row level security;
alter table public.pq_answers enable row level security;
revoke all on public.pq_teachers, public.pq_questions, public.pq_rooms,public.pq_players,public.pq_answers from anon, authenticated;

create function public.pq_teacher_check() returns boolean language plpgsql security definer set search_path='' as $$
begin
 if not exists(select 1 from public.pq_teachers where user_id=auth.uid()) then raise exception 'Conta não autorizada como professor.'; end if;
 return true;
end $$;

create function public.pq_create_room(p_title text,p_count int,p_seconds int) returns uuid language plpgsql security definer set search_path='' as $$
declare rid uuid; qids int[]; invite text;
begin
 perform public.pq_teacher_check();
 if length(trim(p_title)) not between 1 and 60 or p_count not in(5,10,15) or p_seconds not in(0,30,60,90,120) then raise exception 'Configuração inválida.'; end if;
 select array_agg(id order by id) into qids from (select id from public.pq_questions where data->>'curriculum'='poo-v2' order by id limit p_count) q;
 if coalesce(array_length(qids,1),0)<>p_count then raise exception 'Banco de questões incompleto.'; end if;
 loop
 invite:=upper(substr(replace(gen_random_uuid()::text,'-',''),1,6));
 begin
 insert into public.pq_rooms(host,title,code,question_ids,seconds) values(auth.uid(),trim(p_title),invite,qids,p_seconds) returning id into rid;
 exit;
 exception when unique_violation then null;
 end;
 end loop;
 return rid;
end $$;

create function public.pq_history() returns jsonb language plpgsql security definer set search_path='' as $$
begin
 perform public.pq_teacher_check();
 return coalesce((select jsonb_agg(to_jsonb(r) order by r.created_at desc) from(select id,title,code,status,created_at from public.pq_rooms where host=auth.uid()) r),'[]');
end $$;

create function public.pq_join_room(p_code text,p_name text,p_avatar text) returns uuid language plpgsql security definer set search_path='' as $$
declare r public.pq_rooms; existing text;
begin
 if auth.uid() is null then raise exception 'Identifique-se para entrar.'; end if;
 select * into r from public.pq_rooms where code=upper(trim(p_code)) for update;
 if r.id is null then raise exception 'Sala não encontrada. Confira o código.'; end if;
 if exists(select 1 from public.pq_players where room=r.id and user_id=auth.uid()) then return r.id; end if;
 if r.status<>'lobby' then raise exception 'Esta partida já começou.'; end if;
 if r.host=auth.uid() then raise exception 'Use outro navegador para testar como aluno.'; end if;
 if length(trim(p_name)) not between 2 and 24 or p_avatar not in('🧑‍🚀','🦊','🤖','🐸','🐱','🐙') then raise exception 'Nome ou avatar inválido.'; end if;
 if (select count(*) from public.pq_players where room=r.id)>=100 then raise exception 'A sala está cheia.'; end if;
 insert into public.pq_players values(r.id,auth.uid(),trim(p_name),p_avatar);
 return r.id;
 exception when unique_violation then raise exception 'Este apelido já está em uso. Escolha outro.';
end $$;

create function public.pq_advance(p_room uuid,p_expected text,p_current int) returns void language plpgsql security definer set search_path='' as $$
declare r public.pq_rooms;
begin
 select * into r from public.pq_rooms where id=p_room for update;
 if r.host is distinct from auth.uid() or auth.uid() is null then raise exception 'Apenas o professor pode controlar a partida.'; end if;
 if r.status<>p_expected or r.current<>p_current then raise exception 'A sala já avançou. Aguarde a atualização.'; end if;
 if r.status='lobby' and not exists(select 1 from public.pq_players where room=r.id) then raise exception 'Aguarde pelo menos um participante.'; end if;
 if r.status in('lobby','reveal') then
   if r.current+1>=array_length(r.question_ids,1) then update public.pq_rooms set status='finished' where id=r.id;
   else update public.pq_rooms set status='active',current=current+1,started_at=clock_timestamp() where id=r.id; end if;
 elsif r.status='active' then update public.pq_rooms set status='reveal' where id=r.id;
 end if;
end $$;

create function public.pq_answer(p_room uuid,p_question int,p_choice int) returns void language plpgsql security definer set search_path='' as $$
declare r public.pq_rooms;q jsonb;t numeric;duration int;ok boolean;pts int;
begin
 select * into r from public.pq_rooms where id=p_room for update;
 if not exists(select 1 from public.pq_players where room=p_room and user_id=auth.uid()) then raise exception 'Você não participa desta sala.'; end if;
 if r.status<>'active' or r.current<>p_question then raise exception 'Esta questão não está aberta.'; end if;
 if p_choice not between 0 and 3 then raise exception 'Alternativa inválida.'; end if;
 select data into q from public.pq_questions where id=r.question_ids[r.current+1];
 duration:=case when r.seconds=0 then (q->>'seconds')::int else r.seconds end;
 t:=extract(epoch from(clock_timestamp()-r.started_at));
 if t>duration or t<0 then raise exception 'Tempo encerrado.'; end if;
 ok:=p_choice=(q->>'answer')::int;
 pts:=case when ok then 800+round(200*greatest(0,1-t/duration))::int else 0 end;
 insert into public.pq_answers(room,user_id,question,choice,elapsed,correct,points) values(p_room,auth.uid(),p_question,p_choice,t,ok,pts);
 exception when unique_violation then raise exception 'Sua resposta já foi registrada.';
end $$;

create function public.pq_state(p_room uuid) returns jsonb language plpgsql security definer set search_path='' as $$
declare r public.pq_rooms;q jsonb;players jsonb;mine jsonb;dist jsonb;answered int;is_host boolean;
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
 if r.status='active' then q:=q-'answer'-'explanation'; end if;
 end if;
 select jsonb_build_object('choice',a.choice,'points',case when r.status='active' then null else a.points end) into mine from public.pq_answers a where room=p_room and user_id=auth.uid() and question=r.current;
 if is_host and r.status='reveal' then
 select jsonb_agg(n order by i) into dist from(select i,(select count(*) from public.pq_answers where room=p_room and question=r.current and choice=i) n from generate_series(0,3) i) d;
 end if;
 return jsonb_build_object('id',r.id,'title',r.title,'code',r.code,'status',r.status,'current',r.current,'total',array_length(r.question_ids,1),'started_at',r.started_at,'server_now',clock_timestamp(),'duration',case when r.seconds=0 then (q->>'seconds')::int else r.seconds end,'question',q,'is_host',is_host,'players',players,'my_answer',mine,'answered',answered,'distribution',dist);
end $$;

create function public.pq_export(p_room uuid) returns jsonb language plpgsql security definer set search_path='' as $$
declare r public.pq_rooms;result jsonb;
begin
 select * into r from public.pq_rooms where id=p_room;
 if r.host is distinct from auth.uid() or auth.uid() is null then raise exception 'Apenas o professor pode exportar.'; end if;
 select coalesce(jsonb_agg(jsonb_build_object('Aluno',p.name,'Sala',r.code,'Questao',q.data->>'title','Conceito',q.data->>'concept','Resposta',coalesce(q.data->'options'->>a.choice,'Sem resposta'),'Correta',q.data->'options'->>(q.data->>'answer')::int,'Acertou',case when a.correct then 'Sim' else 'Não' end,'Tempo_s',a.elapsed,'Pontos',coalesce(a.points,0)) order by p.name,seq.i),'[]') into result
 from public.pq_players p cross join unnest(r.question_ids) with ordinality seq(qid,i)
 join public.pq_questions q on q.id=seq.qid
 left join public.pq_answers a on a.room=p.room and a.user_id=p.user_id and a.question=seq.i-1
 where p.room=p_room;
 return result;
end $$;

revoke all on function public.pq_teacher_check(),public.pq_create_room(text,int,int),public.pq_history(),public.pq_join_room(text,text,text),public.pq_advance(uuid,text,int),public.pq_answer(uuid,int,int),public.pq_state(uuid),public.pq_export(uuid) from public,anon,authenticated;
grant execute on function public.pq_teacher_check(),public.pq_create_room(text,int,int),public.pq_history(),public.pq_join_room(text,text,text),public.pq_advance(uuid,text,int),public.pq_answer(uuid,int,int),public.pq_state(uuid),public.pq_export(uuid) to authenticated;
commit;
