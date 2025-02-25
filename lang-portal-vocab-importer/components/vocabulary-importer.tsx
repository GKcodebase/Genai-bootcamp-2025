"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { CopyIcon } from "lucide-react"

const groqModels = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it", "mixtral-8x7b-32768"]

export default function VocabularyImporter() {
  const { register, handleSubmit } = useForm()
  const [result, setResult] = useState("")
  const [showAlert, setShowAlert] = useState(false)
  const [selectedModel, setSelectedModel] = useState(groqModels[0])

  const onSubmit = async (data: { category: string }) => {
    try {
      const response = await fetch("/api/generate-vocabulary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model: selectedModel, category: data.category }),
      })

      if (!response.ok) {
        throw new Error("Failed to generate vocabulary")
      }

      const vocabulary = await response.json()
      setResult(JSON.stringify(vocabulary, null, 2))
    } catch (error) {
      console.error("Error:", error)
      setResult("Error generating vocabulary. Please try again.")
    }
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(result).then(() => {
      setShowAlert(true)
      setTimeout(() => setShowAlert(false), 3000)
    })
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="flex space-x-4">
          <Select value={selectedModel} onValueChange={setSelectedModel}>
            <SelectTrigger className="w-[200px]">
              <SelectValue placeholder="Select Groq model" />
            </SelectTrigger>
            <SelectContent>
              {groqModels.map((model) => (
                <SelectItem key={model} value={model}>
                  {model}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Input {...register("category")} placeholder="Enter thematic category" className="flex-grow" />
        </div>
        <Button type="submit">Generate Vocabulary</Button>
      </form>

      {result && (
        <div className="space-y-2">
          <Textarea value={result} readOnly className="h-[300px] font-mono text-sm" />
          <Button onClick={copyToClipboard} className="w-full">
            <CopyIcon className="mr-2 h-4 w-4" /> Copy to Clipboard
          </Button>
        </div>
      )}

      {showAlert && (
        <Alert>
          <AlertDescription>Copied to clipboard successfully!</AlertDescription>
        </Alert>
      )}
    </div>
  )
}

