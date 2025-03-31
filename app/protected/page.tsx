import { createClient } from "@/utils/supabase/server";
import { redirect } from "next/navigation";
import CarForm from "@/components/CarForm";

export default async function ProtectedPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return redirect("/sign-in");
  }

  return (
    <div className="h-screen w-screen bg-gray-50 overflow-hidden">
      <div className="w-full h-full flex flex-col p-6 gap-4">
        <main className="flex-1 overflow-hidden">
          <CarForm />
        </main>
      </div>
    </div>
  );
}
