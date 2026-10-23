-- Encerramento e arquivamento reversível, sem apagar respostas.
begin;
alter table public.pq_rooms add column if not exists archived_at timestamptz;
create or replace function public.pq_close_room(p_room uuid) returns void language plpgsql security definer set search_path='' as $$
declare r public.pq_rooms;
begin
 select * into r from public.pq_rooms where id=p_room for update;
 if auth.uid() is null or r.host is distinct from auth.uid() then raise exception 'Apenas o professor desta sala pode encerrá-la.'; end if;
 update public.pq_rooms set status='finished' where id=p_room;
end $$;
create or replace function public.pq_archive_room(p_room uuid,p_archived boolean) returns void language plpgsql security definer set search_path='' as $$
declare r public.pq_rooms;
begin
 select * into r from public.pq_rooms where id=p_room for update;
 if auth.uid() is null or r.host is distinct from auth.uid() then raise exception 'Apenas o professor desta sala pode arquivá-la.'; end if;
 if p_archived is null then raise exception 'Escolha arquivar ou restaurar.'; end if;
 if p_archived and r.status<>'finished' then raise exception 'Encerre a partida antes de arquivá-la.'; end if;
 update public.pq_rooms set archived_at=case when p_archived then coalesce(archived_at,clock_timestamp()) else null end where id=p_room;
end $$;
create or replace function public.pq_history() returns jsonb language plpgsql security definer set search_path='' as $$
begin
 perform public.pq_teacher_check();
 return coalesce((select jsonb_agg(to_jsonb(r) order by r.created_at desc) from(select id,title,code,status,subject,archived_at,created_at from public.pq_rooms where host=auth.uid()) r),'[]');
end $$;
revoke all on function public.pq_close_room(uuid),public.pq_archive_room(uuid,boolean) from public,anon,authenticated;
grant execute on function public.pq_close_room(uuid),public.pq_archive_room(uuid,boolean) to authenticated;
commit;
