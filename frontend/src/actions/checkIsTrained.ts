'use server';

import {API_URL} from "@/lib/constants";

export async function checkIsTrained() {
  try {
    const response = await fetch(`${API_URL}/is_trained`);
    const data = await response.json();
    const isTrained =  data?.status === 'trained';

    console.log("isTrained", isTrained);
    return isTrained;
  } catch (error) {
    console.error('Error checking if model is trained:', error);
  }
  return false;
}
