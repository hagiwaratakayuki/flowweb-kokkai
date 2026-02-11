<script>
  import { Button, ListGroup } from "@sveltestrap/sveltestrap";

  import { createEventDispatcher } from "svelte";
  import { onMount } from "svelte";
  import ListItem from "./ListItem.svelte";
  import { getTextUrl } from "$lib/url/basic/text";
  const dispatcher = createEventDispatcher();
  export let selectedId = "";
  export let getItemUrl = getTextUrl;

  export function selectItem(id, isScroll = true) {
    if (selectedItem != null) {
      selectedItem.deselect();
    }
    selectedItem = elements[id];
    selectedItem.select(isScroll);
  }
  /**
   * @type {Object.<any, ListItem>}
   */
  let elements = {};
  /**
   * @type {ListItem | null}
   */
  let selectedItem = null;
  /**
   * @type {Overviews}
   */
  let _overviews = [];
  let _isNextExist = false;

  /**
   * @typedef  {import("$lib/ml_api/api_types/TextOverview").TextOverview[]} Overviews
   */
  /**
   *
   * @param {Overviews} overViews
   * @param {bool} isNextExist
   */
  export function addOverviews(overViews, isNextExist) {
    _overviews = _overViews.concat(overViews);
    _isNextExist = isNextExist;
  }
  /**
   *
   * @param {Overviews} overViews
   * @param {bool} isNextExist
   */
  export function setOverviews(overViews, isNextExist) {
    _overviews = overViews;
    _isNextExist = isNextExist;
  }
  function _getNext() {
    dispatcher("next");
  }
  /**
   * @param {CustomEvent} event
   */
  function onMouseEnterItem(event) {
    selectItem(event.detail, false);
    dispatcher("mouseover", event.detail);
  }
</script>

<ListGroup>
  {#each _overviews as overview}
    <ListItem
      {overview}
      {selectedId}
      bind:this={elements[overview.id]}
      on:mouseenter={onMouseEnterItem}
      {getItemUrl}
    />
  {/each}
</ListGroup>

{#if _isNextExist}
  <p class="text-center">
    <Button type="button" color="link" on:click={_getNext}>...more</Button>
  </p>
{/if}
