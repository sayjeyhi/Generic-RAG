import {ChangeEvent, FormEvent, useState} from "react";
import {trainYoutube} from "@/actions/trainYoutube";
import {useRouter} from "next/navigation";

export const useYouTube = () => {
  const [youtubeLink, setYoutubeLink] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const router = useRouter();

  const handleLinkChange = (event: ChangeEvent<HTMLInputElement>) => {
    setYoutubeLink(event.target.value);
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!youtubeLink) {
      alert('Please enter a YouTube link.');
      return;
    }

    setLoading(true);

    try {
      await trainYoutube(youtubeLink)
    } catch (error) {
      console.error('Error uploading:', error);
      alert('Upload failed');
    } finally {
      setLoading(false);
    }

    router.push('/ask');
  };

  return { youtubeLink, loading, handleLinkChange, handleSubmit };
};
