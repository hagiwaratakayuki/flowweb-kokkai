<script>
  import Flow from "./Flow/Flow.svelte";
  import TextList from "$lib/elements/TextOverview/List.svelte";
  import { Row, Col } from "@sveltestrap/sveltestrap";
  import { overviews_to_flow } from "./Flow/overviews_to_flow";
  /**
   * @type {TextList}
   * */
  let textList;
  let _flow;
  let _overViews;
  let _isLoading = true;
  let _isError = false;
  let _isNextExist = false;

  /**
   * @type {Flow}
   */
  let flowComponent;

  export function setInitData(overViews, isNextExist = false) {
    _overViews = overViews;
    _flow = overviews_to_flow(overViews);
    _isLoading = false;
    _isNextExist = isNextExist;
  }
  export function initError() {
    _isLoading = false;
    _isError = true;
  }

  //@todo add flow
  //@todo add additional loading
  export function addOverviews(overViews, isNextExist) {
    if (typeof textList === "undefined") {
      return;
    }
    textList.addOverviews(overViews, isNextExist);
  }
  /**
   * @@param {import("./Flow/Flow.event").NodeEvent} event
   */
  function onNodeOver(event) {
    const { gridInfo } = event.detail;
    textList.selectItem(gridInfo.nodes[0].id);
  }
  /**
   *
   * @param {CustomEvent} event
   */
  function onListItemMouseOver(event) {
    flowComponent.moveToNode(event.detail);
  }
</script>

{#if _isLoading == true}
  loading
{:else if _isError == false}
  <h3 class="mb-3">
    Flow In NASA Scientific and Technical Information Repositry(1971)
  </h3>
  <Row class="flow">
    <Col class="h100" sm="2">
      <div class="sidebar vertical-scroll me-4">
        <TextList
          overViews={_overViews}
          isNextExist={_isNextExist}
          bind:this={textList}
          on:mouseover={onListItemMouseOver}
        />
      </div>
    </Col>
    <Col class="h-100 p-2 border border-primary-subtle rounded-1" sm="10">
      <Flow bind:this={flowComponent} flow={_flow} on:NodeOver={onNodeOver} />
    </Col>
  </Row>
{:else}
  error
{/if}
