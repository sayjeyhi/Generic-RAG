'use server';

import {API_URL} from "@/lib/constants";

export async function checkIsTrained() {
  const response = await fetch(`${API_URL}/is_trained`);
  const data = await response.json();
  return data;
}
