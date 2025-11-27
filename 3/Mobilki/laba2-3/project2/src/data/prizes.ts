export interface Prize {
  category: string;
  date: string;
  grant: string;
}

export const prizes: Prize[] = [
  { category: "Физика", date: "10 декабря 2023", grant: "≈ 11 млн SEK" },
  { category: "Химия", date: "10 декабря 2023", grant: "≈ 11 млн SEK" },
  { category: "Физиология/Медицина", date: "10 декабря 2023", grant: "≈ 11 млн SEK" },
  { category: "Литература", date: "10 декабря 2023", grant: "≈ 11 млн SEK" },
  { category: "Премия мира", date: "10 декабря 2023", grant: "≈ 11 млн SEK" },
  { category: "Экономические науки", date: "10 декабря 2023", grant: "≈ 11 млн SEK" }
];