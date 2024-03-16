<script>
  import Card from "./Card.svelte";
  import { Row, Col, Button } from "@sveltestrap/sveltestrap";
  import { createEventDispatcher } from "svelte";
  const dispatcher = createEventDispatcher();
  export let overViews = null;
  export let isNextExist = null;
  let _isLocked = false;
  $: if (_isLocked == false && overViews !== null && isNextExist !== null) {
    _overviews = overViews;
    _isNextExist = isNextExist;
    _isLocked = true;
  }
  /**
   * @typedef  {import("$lib/ml_api/api_types/TextOverView").TextOverView[]} OverViews
   */
  /**
   *
   * @param {OverViews} overViews
   * @param {bool} isNextExist
   */
  export function addOverView(overViews, isNextExist) {
    _overviews = overViews.concat(overViews);
    _isNextExist = isNextExist;
  }

  /**
   * @type {OverViews}
   */
  let _overviews = [];
  let _isNextExist = false;
  function _getNext() {
    dispatcher("next");
  }
</script>

<Row>
  {#each _overviews as overview}
    <Col md="4" sm="1" class="mb-4">
      <Card {overview} />
    </Col>
  {/each}
</Row>
{#if _isNextExist}
  <p class="text-center">
    <Button type="button" color="link" on:click={_getNext}>...more</Button>
  </p>
{/if}
