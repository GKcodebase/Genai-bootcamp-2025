import { groq } from "@ai-sdk/groq"
import { generateObject } from "ai"
import { z } from "zod"

const vocabularySchema = z.object({
  items: z.array(
    z.object({
      kanji: z.string(),
      romaji: z.array(z.string()), // Update this to match the actual response
      english: z.string(),
      parts: z.array(
        z.object({
          kanji: z.string(),
          romaji: z.array(z.string()),
        }),
      ),
    }),
  ),
})

export async function POST(req: Request) {
  const { model, category } = await req.json()

  try {
    const { object } = await generateObject({
      model: groq(model),
      schema: vocabularySchema,
      prompt: `Generate a list of 10 Japanese vocabulary words related to the category "${category}". Include the kanji, romaji, English translation, and word parts.`,
    })

    return new Response(JSON.stringify(object), {
      headers: { "Content-Type": "application/json" },
    })
  } catch (error) {
    console.error("Error generating vocabulary:", error)
    return new Response(JSON.stringify({ error: "Failed to generate vocabulary" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    })
  }
}

