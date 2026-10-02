import { supabase } from "./supabaseClient";

// Append-only audit trail for admin actions (RLS only allows an admin to
// insert a row with their own admin_id — see migration 0001). Failures are
// logged to the console but never block the admin action itself; the log is
// a record of what happened, not a gate on whether it's allowed to happen.
export async function logAdminAction(adminId, action, targetTable, targetId, details = {}) {
  const { error } = await supabase
    .from("admin_activity_log")
    .insert({ admin_id: adminId, action, target_table: targetTable, target_id: targetId, details });
  if (error) console.error("Failed to write admin_activity_log entry:", error);
}
