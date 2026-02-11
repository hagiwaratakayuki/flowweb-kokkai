<script>
  import Flow from "./Flow.svelte";
  import TextList from "$lib/elements/TextOverview/List.svelte";
  import { Row, Col } from "@sveltestrap/sveltestrap";
  import { overviews_to_flow } from "./overviews_to_flow";
  import Section from "../GuiComponent/Section.svelte";
  import { getTextUrl } from "$lib/url/basic/text";
  /**
   * @type {TextList}
   * */
  let textList;
  let _flow;
  let _overViews;
  let _isError = false;
  let _isNextExist = false;
  export let getItemUrl = getTextUrl;

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
   * @@param {import("./Flow.event").FlowNodeEvent} event
   */
  function onNodeOver(event) {
    const { interactiveData } = event.detail;
    textList.selectItem(interactiveData.nodes[0].id);
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
  <Col class="h100" md="2" sm="12">
    <slot name="sidebar" />
    <Section>
      <slot name="textlist_header"><h2 class="section_header">発言</h2></slot>
      <div class="sidebar vertical-scroll me-4">
        <TextList
          bind:this={textList}
          on:mouseover={onListItemMouseOver}
          {getItemUrl}
        />
      </div>
    </Section>
  </Col>
  <Col class="h-100" md="10" sm="12">
    <slot name="main" />
    <div class="h-100 border border-primary-subtle rounded-1">
      <Flow
        bind:this={flowComponent}
        flow={_flow}
        on:NodeOver={onNodeOver}
        {getItemUrl}
      />
    </div>
  </Col>
</Row>
