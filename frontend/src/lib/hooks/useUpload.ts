import { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';

export const useUpload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

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

  return { file, loading, handleFileChange, handleSubmit };
};
