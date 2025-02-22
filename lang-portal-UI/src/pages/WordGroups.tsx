
import { useState } from "react";
import { ArrowDown, ArrowUp } from "lucide-react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const WordGroups = () => {
  const [sortColumn, setSortColumn] = useState("");
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");
  const [currentPage, setCurrentPage] = useState(1);

  const groups = [
    {
      id: 1,
      name: "Core Verbs",
      wordCount: 50,
    },
    // Add more sample groups as needed
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
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Word Groups</h1>
      
      <div className="bg-white rounded-lg shadow">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead onClick={() => handleSort("name")} className="cursor-pointer">
                Group Name <SortIcon column="name" />
              </TableHead>
              <TableHead onClick={() => handleSort("wordCount")} className="cursor-pointer text-right">
                # Words <SortIcon column="wordCount" />
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {groups.map((group) => (
              <TableRow key={group.id}>
                <TableCell>
                  <a href={`/groups/${group.id}`} className="hover:text-primary">
                    {group.name}
                  </a>
                </TableCell>
                <TableCell className="text-right">{group.wordCount}</TableCell>
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

export default WordGroups;
