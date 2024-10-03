'use server';

import {API_URL} from "@/lib/constants";

export async function askQuestion(question: string) {
  console.log("Asking", question);
  const response = await fetch(`${API_URL}/ask`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question: question,
    }),
  });
  const data = await response.json();
  console.log("Answer: ", data)
  return data?.answer || '';
}
