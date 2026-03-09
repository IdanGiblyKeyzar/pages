# Keyzar — Phase 1: Platform Foundations

Before touching the Keyzar codebase, build fluency in the platform underneath. By the end of this phase you should be able to trace how a URL becomes a rendered product page in Hydrogen, write Storefront API queries by hand, and understand the SSR lifecycle.

---

## 1. Shopify Mental Model

You're a headless frontend engineer — Shopify is your data and commerce backend.

- **Products → Variants → Collections → Metafields** — the core data model. A product has variants (Yellow Gold / White Gold), belongs to collections (Engagement Rings), and can have metafields for custom data.
- **Storefront API** — the only API our frontend talks to. Separate from the Admin API (which manages the store behind the scenes).
- **Headless** — Shopify handles cart, checkout, inventory, payments. We own the entire frontend experience.

**Read:** [Headless overview](https://shopify.dev/docs/storefronts/headless) · [Storefront API guide](https://shopify.dev/docs/api/storefront)

**Self-check:** Can you explain the product → variant → collection relationship and what data the Storefront API exposes?

---

## 2. React Router & SSR

Hydrogen is built on Remix (React Router v7). Understand the routing and rendering model first.

**React Router:**

- **File-based routing** — file names → URL segments, nested routes, dynamic params (`$handle`)
- **`loader` / `action`** — loaders fetch data on the server before render, actions handle mutations. This is the core data flow at Keyzar — not `useEffect`.
- **`useLoaderData`, `useNavigation`** — connect components to server data and navigation state
- **Nested routes + `<Outlet>`** — parent layouts persist while child routes swap
- **`useSearchParams`** — URL params as reactive state. How Keyzar handles filters, sorting, pagination — not `useState`. Survives refreshes, works with SSR, is shareable.

**SSR:**

- **Timeline:** server render → HTML sent → paint → JS loads → hydration → interactive
- **Why it matters:** faster first paint (conversion), SEO, better Core Web Vitals
- **Streaming:** `defer` / `Await` — stream the shell, fill in slow data after
- **Pitfalls:** server/client HTML must match. Browser APIs (`window`, `document`) don't exist on the server — use `useEffect` or `typeof window` guards.

**Do:** Build a small app with nested routes, a loader, and `useSearchParams`. Disable JS and see the SSR output.

**Read:** [React Router v7 docs](https://reactrouter.com/home) · [How Hydrogen uses Remix](https://shopify.dev/docs/storefronts/headless/hydrogen/project-structure)

**Self-check:** `loader` vs. `useEffect` — what's the difference? Why `useSearchParams` over `useState` for filters?

---

## 3. Hydrogen

Commerce-specific layer on top of Remix.

- **Route loaders** — fetch from the Storefront API via `context.storefront.query()` inside loaders
- **Built-in components** — `<Image>` (optimized, prevents CLS), `<Money>` (currency formatting), `<CartProvider>` (cart state via actions)
- **Caching** — `CacheLong`, `CacheShort`, `CacheNone` control data freshness

**Do:** Complete the [Hydrogen tutorial](https://shopify.dev/docs/storefronts/headless/hydrogen/getting-started) — build a collection page and product detail page.

**Self-check:** Trace the full lifecycle: URL → route → loader → API query → SSR → hydration → interactive.

---

## 4. Storefront API & GraphQL

The API behind every page. Every product image, price, variant, and filter comes through here.

- **Write queries by hand** in the GraphiQL explorer — build the muscle memory
- **`collection.products` filters** — server-side filtering by price, product type, variant options
- **Cursor-based pagination** — `first`/`after`, `pageInfo.hasNextPage`. Not page numbers.
- **Traps:** `priceRange` = min/max across all variants (not a specific variant's price); `availableForSale` = true if *any* variant is available

**Do:** Open GraphiQL (Shopify admin → Apps → Headless), write queries, filter a collection, paginate with cursors, break things on purpose.

**Read:** [Storefront API reference](https://shopify.dev/docs/api/storefront)

**Self-check:** Can you write a filtered, paginated collection query from memory?

---

## Checklist

All checked before moving to Phase 2.

- [ ] Understand Shopify's product/variant/collection data model
- [ ] Built a React Router app with loaders, nested routes, `useSearchParams`
- [ ] Can explain the SSR lifecycle and hydration
- [ ] Completed the Hydrogen tutorial
- [ ] Can write Storefront API queries independently
- [ ] Understand cursor pagination and server-side filtering
