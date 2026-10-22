-- Execute após 02-questions.sql no projeto já instalado.
-- Mantém os IDs das questões das partidas antigas.
begin;
create or replace function public.pq_create_room(p_title text,p_count int,p_seconds int) returns uuid language plpgsql security definer set search_path='' as $$
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
commit;
