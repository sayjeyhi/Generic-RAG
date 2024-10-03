import Trainer from "./_components/trainer";
import {checkIsTrained} from "@/actions/checkIsTrained";
import {redirect} from "next/navigation";

export const dynamic = 'force-dynamic'

export default async function Home() {
  const isTrained = await checkIsTrained();

  if (isTrained) {
    console.log("Redirecting to ask", isTrained);
    return redirect("/ask");
  }

  return (
    <Trainer/>
  );
}


