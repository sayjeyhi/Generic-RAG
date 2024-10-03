'use server';

import {API_URL} from "@/lib/constants";

export async function trainYoutube(link: string) {
  console.log("YOU TUBE link", link);
  const response = await fetch(`${API_URL}/train`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      youtube_link: link,
    }),
  });
  const data = await response.json();
  console.log("Trained", data);
  return data;
}
