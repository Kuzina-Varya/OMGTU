// src/types/nobel.types.ts

import * as t from 'io-ts';

// --- Лауреат внутри премии (в /prize.json) ---
const LaureateInPrize = t.type({
  id: t.string,
  firstname: t.union([t.string, t.undefined]),
  surname: t.union([t.string, t.undefined]),
  motivation: t.union([t.string, t.undefined]),
  share: t.union([t.string, t.undefined]),
});

// --- Премия ---
export const NobelPrizeCodec = t.type({
  year: t.string,
  category: t.string,
  // overallMotivation есть НЕ у всех премий → необязательное
  overallMotivation: t.union([t.string, t.undefined]),
  // laureates — может отсутствовать (редко, но бывает)
  laureates: t.union([t.array(LaureateInPrize), t.undefined]),
});

export type NobelPrize = t.TypeOf<typeof NobelPrizeCodec>;

// --- Ответ API: /prize.json ---
export const PrizesResponseCodec = t.type({
  prizes: t.array(NobelPrizeCodec),
});

export type PrizesResponse = t.TypeOf<typeof PrizesResponseCodec>;

// --- Премия внутри лауреата (в /laureate.json) ---
const PrizeInLaureate = t.type({
  year: t.string,
  category: t.string,
  // в laureate.json нет motivation/share
});

// --- Лауреат ---
export const NobelLaureateCodec = t.type({
  id: t.string,
  firstname: t.union([t.string, t.undefined]),
  surname: t.union([t.string, t.undefined]),
  born: t.union([t.string, t.undefined]),
  died: t.union([t.string, t.undefined]),
  gender: t.union([t.string, t.undefined]),
  prizes: t.array(PrizeInLaureate),
});

export type NobelLaureate = t.TypeOf<typeof NobelLaureateCodec>;

// --- Ответ API: /laureate.json ---
export const LaureatesResponseCodec = t.type({
  laureates: t.array(NobelLaureateCodec),
});

export type LaureatesResponse = t.TypeOf<typeof LaureatesResponseCodec>;