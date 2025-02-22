
import { useState } from "react";
import { ArrowDown, ArrowUp, Play } from "lucide-react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const Words = () => {
  const [sortColumn, setSortColumn] = useState("");
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");
  const [currentPage, setCurrentPage] = useState(1);

  const words = [
    {
      id: 1,
      japanese: "始める",
      romaji: "hajimeru",
      english: "to begin",
      correct: 15,
      wrong: 3,
    },
    // Add more sample words as needed
  ];

  const handleSort = (column: string) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortDirection("asc");
    }
  };

  const SortIcon = ({ column }: { column: string }) => {
    if (sortColumn !== column) return null;
    return sortDirection === "asc" ? (
      <ArrowDown className="inline w-4 h-4 ml-1" />
    ) : (
      <ArrowUp className="inline w-4 h-4 ml-1" />
    );
  };

  return (
    <div className="animate-fadeIn">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Words</h1>
      
      <div className="bg-white rounded-lg shadow">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead onClick={() => handleSort("japanese")} className="cursor-pointer">
                Japanese <SortIcon column="japanese" />
              </TableHead>
              <TableHead onClick={() => handleSort("romaji")} className="cursor-pointer">
                Romaji <SortIcon column="romaji" />
              </TableHead>
              <TableHead onClick={() => handleSort("english")} className="cursor-pointer">
                English <SortIcon column="english" />
              </TableHead>
              <TableHead onClick={() => handleSort("correct")} className="cursor-pointer text-right">
                # Correct <SortIcon column="correct" />
              </TableHead>
              <TableHead onClick={() => handleSort("wrong")} className="cursor-pointer text-right">
                # Wrong <SortIcon column="wrong" />
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {words.map((word) => (
              <TableRow key={word.id}>
                <TableCell className="font-jp">
                  <div className="flex items-center gap-2">
                    <button className="p-1 hover:bg-gray-100 rounded-full">
                      <Play className="w-4 h-4" />
                    </button>
                    <a href={`/words/${word.id}`} className="hover:text-primary">
                      {word.japanese}
                    </a>
                  </div>
                </TableCell>
                <TableCell>{word.romaji}</TableCell>
                <TableCell>{word.english}</TableCell>
                <TableCell className="text-right">{word.correct}</TableCell>
                <TableCell className="text-right">{word.wrong}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        <div className="flex items-center justify-between px-4 py-3 border-t">
          <button
            className="px-3 py-1 rounded bg-secondary disabled:opacity-50"
            disabled={currentPage === 1}
            onClick={() => setCurrentPage(currentPage - 1)}
          >
            Previous
          </button>
          <span className="text-sm text-gray-700">
            Page <span className="font-medium">{currentPage}</span> of <span className="font-medium">3</span>
          </span>
          <button
            className="px-3 py-1 rounded bg-secondary disabled:opacity-50"
            disabled={currentPage === 3}
            onClick={() => setCurrentPage(currentPage + 1)}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default Words;
