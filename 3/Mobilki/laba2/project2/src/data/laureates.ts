export interface Laureate {
  name: string;
  birth: string;
  prizes: number;
}

export const laureates: Laureate[] = [
  { name: "Мари Кюри", birth: "7 ноября 1867", prizes: 2 },
  { name: "Линус Полинг", birth: "28 февраля 1901", prizes: 2 },
  { name: "Джон Бардин", birth: "23 мая 1908", prizes: 2 },
  { name: "Комитет против насилия (организация)", birth: "основан 1980", prizes: 1 },
  { name: "Абдулразак Гурна", birth: "20 декабря 1948", prizes: 1 }
];