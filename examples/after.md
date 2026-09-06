# Why we moved the build pipeline to GitHub Actions

Our old pipeline took 40 minutes and failed about one run in five for reasons nobody could reproduce. People stopped reading the red X. When a build failed for real, it sat for hours because everyone assumed it was the usual flake.

We looked at three options and picked GitHub Actions, mostly because the runners are already next to the code and we stopped maintaining a separate box. The migration took two weeks, and the first week of it was spent finding out that four of our tests depended on a shared temp directory the old runner never cleaned.

Builds now finish in eight minutes. The failure rate over the last 60 runs is two, and both were real.

The part I'd do differently: we ported the old workflow first and cleaned it up after, which meant we carried the shared-state bug into the new system and debugged it twice. Fixing the tests first would have cost three days and saved a week.
