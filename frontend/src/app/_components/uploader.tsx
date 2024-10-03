"use client";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import { useUpload } from "@/lib/hooks/useUpload";
import { useYouTube } from "@/lib/hooks/useYouTube";

export default function Uploader() {
  const { file, loading: uploadLoading, handleFileChange, handleSubmit: handleUploadSubmit } = useUpload();
  const { youtubeLink, loading: youtubeLoading, handleLinkChange, handleSubmit: handleYouTubeSubmit } = useYouTube();

  return (
    <Tabs defaultValue="upload" className="w-[400px]">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="upload">Upload file</TabsTrigger>
        <TabsTrigger value="youtube">Youtube link</TabsTrigger>
      </TabsList>

      <TabsContent value="upload">
        <Card>
          <CardHeader>
            <CardTitle>Upload file</CardTitle>
            <CardDescription>
              You can upload a file then the file will be processed and you can ask questions
              about it.
            </CardDescription>
          </CardHeader>
          <form onSubmit={handleUploadSubmit}>
            <CardContent className="space-y-2">
              <div className="space-y-1">
                <Label htmlFor="file">File (zip, csv, pdf)</Label>
                <Input id="file" type="file" accept=".zip,.csv,.pdf" onChange={handleFileChange} />
              </div>
            </CardContent>
            <CardFooter>
              <Button type="submit" disabled={uploadLoading}>
                {uploadLoading ? 'Uploading...' : 'Upload'}
              </Button>
            </CardFooter>
          </form>
        </Card>
      </TabsContent>

      <TabsContent value="youtube">
        <Card>
          <CardHeader>
            <CardTitle>Youtube link</CardTitle>
            <CardDescription>
              You can paste a YouTube link and the file will be processed and you
              can ask questions about it.
            </CardDescription>
          </CardHeader>
          <form onSubmit={handleYouTubeSubmit}>
            <CardContent className="space-y-2">
              <div className="space-y-1">
                <Label htmlFor="youtube">YouTube link</Label>
                <Input id="youtube" type="text" value={youtubeLink} onChange={handleLinkChange} />
              </div>
            </CardContent>
            <CardFooter>
              <Button type="submit" disabled={youtubeLoading}>
                {youtubeLoading ? 'Submitting...' : 'Submit'}
              </Button>
            </CardFooter>
          </form>
        </Card>
      </TabsContent>
    </Tabs>
  );
}
