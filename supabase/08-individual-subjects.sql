-- Só HTML e Só CSS, bancos inéditos e independentes. Aplicar após a carga 02.
begin;
alter table public.pq_rooms drop constraint if exists pq_rooms_subject_check;
alter table public.pq_rooms add constraint pq_rooms_subject_check check(subject in('python','html-css','html','css'));
create or replace function public.pq_create_subject_room(p_title text,p_count int,p_seconds int,p_pack text,p_reflections boolean,p_subject text) returns uuid language plpgsql security definer set search_path='' as $$
declare rid uuid;qids int[];invite text;available int;curriculum text;
begin
 perform public.pq_teacher_check();
 if p_subject is null or p_subject not in('python','html-css','html','css') then raise exception 'Escolha uma modalidade válida.'; end if;
 curriculum:=case p_subject when 'python' then 'poo-v3' when 'html-css' then 'web-v1' when 'html' then 'html-v1' else 'css-v1' end;
 if p_title is null or length(trim(p_title)) not between 1 and 60 or p_count is null or p_count<1 or p_seconds is null or p_seconds not in(0,30,60,90,120,180) or p_pack is null or p_pack not in('mixed','quiz','classify','repair','reflect','visual','selectors','structure') then raise exception 'Configuração inválida.'; end if;
 select count(*) into available from public.pq_questions where data->>'curriculum'=curriculum
 and (p_pack='mixed' or data->>'activity'=p_pack or (p_pack='reflect' and data->>'activity'='quiz' and coalesce(data->>'reflection_prompt','')<>''));
 if available=0 or p_count>available or (p_count not in(5,10,15) and p_count<>available) then raise exception 'Quantidade inválida para esta atividade.'; end if;
 select array_agg(id order by pos) into qids from(select id,(data->>'position')::int pos from public.pq_questions where data->>'curriculum'=curriculum
 and (p_pack='mixed' or data->>'activity'=p_pack or (p_pack='reflect' and data->>'activity'='quiz' and coalesce(data->>'reflection_prompt','')<>'')) order by (data->>'position')::int limit p_count) q;
 loop
 invite:=upper(substr(replace(gen_random_uuid()::text,'-',''),1,6));
 begin
 insert into public.pq_rooms(host,title,code,question_ids,seconds,reflections_enabled,activity_pack,subject)
 values(auth.uid(),trim(p_title),invite,qids,p_seconds,p_pack='reflect' or coalesce(p_reflections,true),p_pack,p_subject) returning id into rid;
 exit;
 exception when unique_violation then null;
 end;
 end loop;
 return rid;
end $$;


create or replace function public.pq_export(p_room uuid) returns jsonb language plpgsql security definer set search_path='' as $$
declare r public.pq_rooms;result jsonb;
begin
 select * into r from public.pq_rooms where id=p_room;
 if r.host is distinct from auth.uid() or auth.uid() is null then raise exception 'Apenas o professor pode exportar.'; end if;
 select coalesce(jsonb_agg(jsonb_build_object('Aluno',p.name,'Conteudo',case r.subject when 'html-css' then 'HTML e CSS' when 'html' then 'Só HTML' when 'css' then 'Só CSS' else 'Python · POO' end,'Sala',r.code,'Questao',q.data->>'title','Conceito',q.data->>'concept','Tipo',coalesce(q.data->>'kind','Quiz'),'Resposta',coalesce(q.data->'options'->>a.choice,'Sem resposta'),'Correta',q.data->'options'->>(q.data->>'answer')::int,'Acertou',case when a.correct then 'Sim' else 'Não' end,'Tempo_s',a.elapsed,'Pontos',coalesce(a.points,0),'Pergunta_explicacao',case when r.reflections_enabled then coalesce(q.data->>'reflection_prompt','') else '' end,'Justificativa',coalesce(f.text,'')) order by p.name,seq.i),'[]') into result
 from public.pq_players p cross join unnest(r.question_ids) with ordinality seq(qid,i)
 join public.pq_questions q on q.id=seq.qid
 left join public.pq_answers a on a.room=p.room and a.user_id=p.user_id and a.question=seq.i-1
 left join public.pq_reflections f on f.room=p.room and f.user_id=p.user_id and f.question=seq.i-1
 where p.room=p_room;
 return result;
end $$;


commit;
