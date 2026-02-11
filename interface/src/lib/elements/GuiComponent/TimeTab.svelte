<script>
  import { Nav, NavItem, NavLink } from "@sveltestrap/sveltestrap";
  import { createEventDispatcher, onMount } from "svelte";
  const dispatcher = createEventDispatcher();

  export let hasNext = false;
  export let hasPrev = false;
  /**
   * @type {"flow" | "categoryword"}
   */
  export let tab;

  onMount(function () {
    if (!tab) {
      const hash = window?.location?.hash;
      if (hash) {
        tab = hash;
      }
    }
    if (!tab === true || (tab !== "flow" && tab !== "categryword")) {
      tab = "flow";
    }
  });

  function clickNavFlow() {
    if (tab === "flow") {
      return;
    }
    tab = "flow";
    dispatcher("clickFlow");
  }
  function clickCategoryword() {
    if (tab === "categoryword") {
      return;
    }
    tab = "categoryword";
    dispatcher("clickCategoryWord");
  }
  function clickNext() {
    dispatcher("next");
  }
  function clickPrev() {
    dispatcher("prev");
  }
</script>

<Nav underline>
  <NavItem>
    <NavLink
      href="#flow"
      active={tab === "flow"}
      on:click={clickNavFlow}
      class={tab === "flow" ? "arrow" : ""}
    >
      Flow
    </NavLink>
  </NavItem>
  <NavItem>
    <NavLink
      href="#categoryword"
      active={tab === "categoryword"}
      on:click={clickCategoryword}
      class={tab === "categoryword" ? "arrow" : ""}
    >
      Catgoryword
    </NavLink>
  </NavItem>
</Nav>
<div class="container mb-3">
  <div class="row justify-content-center">
    <div class="col-auto">
      <button
        class="bg-white guid"
        class:disabled={hasPrev === false}
        on:click={clickPrev}
      >
        <span
          class="d-inline-block guid left"
          class:bg-primary={hasPrev}
          class:bg-dark-subtle={hasPrev === false}
        />
      </button>
    </div>
    <div class="col-auto">
      <slot name="controll" />
    </div>
    <div class="col-auto">
      <button
        class="bg-white guid"
        class:disabled={hasNext === false}
        on:click={clickNext}
      >
        <span
          class="d-inline-block guid right"
          class:bg-primary={hasNext}
          class:bg-dark-subtle={hasNext === false}
        />
      </button>
    </div>
  </div>
</div>
<div class:d-none={tab !== "flow"}>
  <slot name="flow" />
</div>
<div class:d-none={tab !== "categoryword"}>
  <slot name="categryword" />
</div>

<style>
  .guid {
    width: 1em;
    height: 1em;
    border: none;
  }
  .disabled {
    cursor: not-allowed;
  }

  .right {
    clip-path: polygon(0 0, 100% 50%, 0 100%);
  }

  .left {
    clip-path: polygon(0 50%, 100% 0, 100% 100%);
  }
</style>
