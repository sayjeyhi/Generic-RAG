import {ChangeEvent, FormEvent, useState} from "react";
import axios from "axios";

export const useYouTube = () => {
  const [youtubeLink, setYoutubeLink] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const handleLinkChange = (event: ChangeEvent<HTMLInputElement>) => {
    setYoutubeLink(event.target.value);
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!youtubeLink) {
      alert('Please enter a YouTube link.');
      return;
    }

    const formData = new FormData();
    formData.append('youtubeLink', youtubeLink);

    setLoading(true);

    try {
      const response = await axios.post('https://your-server-endpoint.com/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Upload successful');
      console.log(response.data);
    } catch (error) {
      console.error('Error uploading:', error);
      alert('Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return { youtubeLink, loading, handleLinkChange, handleSubmit };
};
