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
    <div class="d-flex flex-row">
      {#if isSelected == true}
        <div class="selected icon align-self-center">●</div>
      {:else}
        <div class="icon align-self-center">◇</div>
      {/if}
      <div>{overview.title.slice(0, 15)}...</div>
    </div>
  </BaseLink>
</li>

<style>
  .icon {
    text-align: center;
    margin-left: 0.25em;
    margin-right: 0.25em;
  }

  .selected {
    color: var(--bs-teal);
  }
</style>
