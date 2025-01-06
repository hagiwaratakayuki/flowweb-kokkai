<script>
  import { onMount, createEventDispatcher } from "svelte";
  import { FlowController, FlowControllerBuilder } from "./flexflow_controller";
  import { browser } from "$app/environment";
  import Tooltip from "./ToolTip.svelte";
  import NodeModal from "./NodeModal.svelte";
  import ToolTip from "./ToolTip.svelte";
  import { getTextUrl } from "$lib/url/basic/text";

  const dispatcher = createEventDispatcher();
  /**
   * @param {import("src/relay_types/flow").DataTransfer}
   * */
  export let flow = {};

  let isMounted = false;

  onMount(function () {
    isMounted = true;
  });
  $: if (
    browser === true &&
    isMounted === true &&
    !flow === false &&
    Object.keys(flow).length > 0
  ) {
    createFlowNetwork(flow).then(function () {
      //console.log("ok");
    });
  }
  /**
   * @type {FlowController}
   */
  let controller;
  let reset;
  /**
   * @type {HTMLElement | null}
   */
  let container = null;
  /**
   * @type {HTMLElement}
   */
  let containerRoot = null;

  let isToolTipVisible = false;
  let tooltipMessage = "";
  let tooltipPosition = { top: 0, left: 0 };
  export let getItemUrl = getTextUrl;
  export function moveToNode(nodeId) {
    if (!controller == false) {
      controller.moveToNode(nodeId);
    }
  }

  /**
   *
   * @param {import("$lib/relay_types/flow").DataTransfer} data
   */
  async function createFlowNetwork(data) {
    if (!reset === false) {
      reset();
    }

    [controller, reset] = await FlowControllerBuilder(container);

    controller.setData(data.nodes, data.edges);
    controller.on("node.over", onNodeOver);
    controller.on("node.over.out", onNodeOverOut);
    controller.on("node.click", onNodeClick);
  }
  /**
   * @type {ToolTip}
   */
  let toolTip;
  /**
   * @typedef {import("./Flow.event").FlowNodeEventMessage} FlowNodeEventMessage
   */

  let isSelected = false;
  /**
   * @param {FlowNodeEventMessage} message
   */
  function onNodeOver(message) {
    isSelected = true;
    tooltipMessage = `${message.interactiveData.nodes[0].title.slice(0, 10)}…`;
    if (message.interactiveData.isOverwraped) {
      tooltipMessage += ` + ${message.interactiveData.nodes.length - 1} articles`;
    }

    toolTip.show(message.x, message.y, tooltipMessage);

    dispatcher("NodeOver", message);
  }
  /**
   *@param {FlowNodeEventMessage}
   */
  function onNodeOverOut(message) {
    toolTip.hide();
    isSelected = false;

    dispatcher("NodeOverOut", message);
  }
  /**
   * @type {NodeModal}
   */
  let nodeModal;
  /**
   * @param {FlowNodeEventMessage} message
   */
  function onNodeClick(message) {
    nodeModal.open(message.interactiveData);
    toolTip.hide();
    dispatcher("NodeClick", message);
  }
  // gurd function for prpagation to body
  function voidFunc() {}
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
  class="flow_container root"
  bind:this={containerRoot}
  class:node_selected={isSelected}
>
  <div class="flow_container" bind:this={container} />
  <NodeModal bind:this={nodeModal} {getItemUrl} />
</div>
<Tooltip bind:this={toolTip} flowElement={containerRoot} />

<style>
  .node_selected {
    cursor: pointer;
  }
  .root {
    position: relative;
    top: 0%;
    left: 0%;
  }
  .flow_container {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: white;
  }
</style>
