<script>
  import TrendLine from "./TrendLine.svelte";
  import { createEventDispatcher } from "svelte";
  const dispatcher = createEventDispatcher();

  export let hasNext = false;
  export let hasPrev = false;
  /**
   *
   * @param {TrendLine} datas
   */
  export function setData(datas) {
    trendLine.setData(datas);
  }

  /**
   * @type {TrendLine}
   */
  let trendLine;

  function clickNext() {
    dispatcher("next");
  }
  function clickPrev() {
    dispatcher("prev");
  }
</script>

<div class="container">
  <div class="row justify-content-center">
    <div class="col-auto">
      <button class="bg-white" on:click={clickPrev}>
        <span
          class="d-inline-block guid left"
          class:bg-primary={hasPrev}
          class:bg-dark-subtle={hasPrev === false}
        />
      </button>
    </div>
    <div class="col-auto">
      <slot />
    </div>
    <div class="col-auto">
      <button class="bg-white guid" on:click={clickNext}>
        <span
          class="d-inline-block guid right"
          class:bg-primary={hasNext}
          class:bg-dark-subtle={hasNext === false}
        />
      </button>
    </div>
  </div>
</div>
<TrendLine bind:this={trendLine} />
<div />

<style>
  .guid {
    width: 1em;
    height: 1em;
    border: none;
  }

  .right {
    clip-path: polygon(0 0, 100% 50%, 0 100%);
  }

  .left {
    clip-path: polygon(0 50%, 100% 0, 100% 100%);
  }
</style>
