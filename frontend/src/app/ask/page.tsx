import {Card, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";

import {checkIsTrained} from "@/actions/checkIsTrained";
import AskForm from "@/app/ask/_components/form";
import {redirect} from "next/navigation";

export const dynamic = 'force-dynamic'

export default async function Ask() {
  const isTrained = await checkIsTrained();
  if(!isTrained) {
    return redirect("/");
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>🎉Model is trained</CardTitle>
        <CardDescription>
          You can now ask questions to the model.
        </CardDescription>
      </CardHeader>
      <AskForm />
    </Card>
  );
}
