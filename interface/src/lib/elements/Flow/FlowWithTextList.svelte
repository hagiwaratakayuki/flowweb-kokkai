<script>
  import Flow from "./Flow.svelte";
  import TextList from "$lib/elements/TextOverview/List.svelte";
  import { Row, Col } from "@sveltestrap/sveltestrap";
  import { overviews_to_flow } from "./overviews_to_flow";
  /**
   * @type {TextList}
   * */
  let textList;
  let _flow;
  let _overViews;
  let _isError = false;
  let _isNextExist = false;

  /**
   * @type {Flow}
   */
  let flowComponent;

  export function setInitData(overViews, isNextExist = false) {
    _flow = overviews_to_flow(overViews);
    textList.setOverviews(overViews, isNextExist);
  }
  export function initError() {
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
   * @@param {import("./Flow.event").NodeEvent} event
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

<Row class="flow">
  <Col class="h100" sm="2">
    <div class="sidebar vertical-scroll me-4">
      <TextList bind:this={textList} on:mouseover={onListItemMouseOver} />
    </div>
  </Col>
  <Col class="h-100 p-2 border border-primary-subtle rounded-1" sm="10">
    <Flow bind:this={flowComponent} flow={_flow} on:NodeOver={onNodeOver} />
  </Col>
</Row>
