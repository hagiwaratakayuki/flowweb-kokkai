<script>
  import { createEventDispatcher } from "svelte";

  const dispatcher = createEventDispatcher();
  export function select(isScroll = true) {
    isSelected = true;
    if (isScroll === true) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  }

  export function deselect() {
    isSelected = false;
  }

  let isSelected = false;
  /**
   * @type  {import("$lib/ml_api/api_types/TextOverview").TextOverview}
   */
  export let overview;
  /**
   * @type {HTMLElement}
   */
  let element;

  function onMouseEnter() {
    dispatcher("mouseenter", overview.id);
  }
</script>

<li
  class="list-group-item border-start-0 border-end-0"
  bind:this={element}
  on:mouseenter={onMouseEnter}
>
  <a href="/text/{overview.id}" class:selected={isSelected}>
    {overview.title.slice(0, 15)}...
  </a>
</li>

<style>
  a {
    text-decoration: none;
    display: inline-block;
  }
  a::before {
    content: "◇";
    margin-right: 1rem;
  }
  li:hover {
    background-color: var(--bs-secondary-bg-subtle);
    border-radius: var(--bs-border-radius-sm);
  }
  a.selected::before {
    content: "●";
    color: var(--bs-teal);
  }
</style>
