-- Novos jogos sem alterar salas existentes. Aplicar após a carga 02.
begin;
create or replace function public.pq_create_subject_room(p_title text,p_count int,p_seconds int,p_pack text,p_reflections boolean,p_subject text) returns uuid language plpgsql security definer set search_path='' as $$
declare rid uuid;qids int[];invite text;available int;curriculum text;
begin
 perform public.pq_teacher_check();
 if p_subject is null or p_subject not in('python','html-css') then raise exception 'Escolha Python ou HTML e CSS.'; end if;
 curriculum:=case when p_subject='python' then 'poo-v3' else 'web-v1' end;
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


commit;
