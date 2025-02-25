import VocabularyImporter from "@/components/vocabulary-importer"

export default function Home() {
  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Japanese Vocabulary Importer</h1>
      <VocabularyImporter />
    </main>
  )
}

