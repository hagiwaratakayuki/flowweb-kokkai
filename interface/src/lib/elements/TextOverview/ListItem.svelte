<script>
  import { createEventDispatcher } from "svelte";
  import { getTextUrl } from "$lib/url/basic/text";
  import BaseLink from "$lib/url/BaseLink.svelte";
  const dispatcher = createEventDispatcher();
  export function select(isScroll = true) {
    isSelected = true;
    if (isScroll === true) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  }
  export let getItemUrl = getTextUrl;
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
  <BaseLink url={getItemUrl(overview.id)}>
    {#if isSelected == true}<span class="selected icon">〇</span>
    {:else}
      <span class="icon">◇</span>
    {/if}
    <span>{overview.title.slice(0, 15)}...</span>
  </BaseLink>
</li>

<style>
  .icon {
    margin-right: 1rem;
  }
  li:hover {
    background-color: var(--bs-secondary-bg-subtle);
    border-radius: var(--bs-border-radius-sm);
  }
  .selected::before {
    color: var(--bs-teal);
  }
</style>
