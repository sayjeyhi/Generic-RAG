'use client';

import { CardContent, CardFooter} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import {Textarea} from "@/components/ui/textarea";
import {Button} from "@/components/ui/button";
import {askQuestion} from "@/actions/ask";
import {FormEvent, useState} from "react";
import {useRouter} from "next/navigation";

export default function AskForm() {
  const [isThinking, setIsThinking] = useState(false);
  const [answer, setAnswer] = useState('');
  const router = useRouter();

  const handleAskSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setIsThinking(true);
    const question = event.target.elements.question.value;
    const answer = await askQuestion(question);
    setAnswer(answer);
    setIsThinking(false);
  };

  const handleTrainAgain = () => {
    router.replace('/train');
  }

  return (
    <form onSubmit={handleAskSubmit} method="post">
      <CardContent className="space-y-2">
        <div className="space-y-1">
          <Label htmlFor="question">Questions</Label>
          <Textarea id="question" placeholder="Ask a question" rows={4} />
        </div>
        <div className="max-w-2xl">
        {answer.length > 0 ? answer : ''}
        </div>
      </CardContent>
      <CardFooter>
        <Button type="submit" disabled={isThinking}>
          {isThinking ? 'Thinking...' : 'Ask'}
        </Button>
        <Button variant="ghost" type="button" onClick={handleTrainAgain}>
          Train again
        </Button>
      </CardFooter>
    </form>
  );
}
