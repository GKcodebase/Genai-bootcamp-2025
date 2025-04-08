# Component Documentation

## Layout Components

### MainLayout
The root layout component that provides the base structure for all pages.
```tsx
<MainLayout>
  <Sidebar />
  <MainContent />
</MainLayout>
```

### Sidebar
Navigation sidebar with links to main sections.
- Dashboard
- Study Activities
- Words
- Groups
- Settings

### Header
Top navigation bar with:
- Theme toggle
- User profile
- Notifications

## UI Components

### StudyCard
```tsx
<StudyCard
  title="Vocabulary Quiz"
  description="Practice your Japanese vocabulary"
  progress={75}
  lastStudied="2024-04-08"
/>
```

### WordList
```tsx
<WordList
  words={words}
  onSort={handleSort}
  onFilter={handleFilter}
/>
```

### GroupGrid
```tsx
<GroupGrid
  groups={groups}
  onGroupSelect={handleGroupSelect}
/>
```

### ProgressChart
```tsx
<ProgressChart
  data={studyData}
  period="weekly"
/>
```