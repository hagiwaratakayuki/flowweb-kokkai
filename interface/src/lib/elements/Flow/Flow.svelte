<script>
  import { onMount, createEventDispatcher } from "svelte";
  import { FlowController, FlowControllerBuilder } from "./flow";
  import { browser } from "$app/environment";
  import Tooltip from "./ToolTip.svelte";
  import NodeModal from "./NodeModal.svelte";
  import ToolTip from "./ToolTip.svelte";
  /**
   * @typedef {import("./Flow.event").NodeEventMessage} EventMessage
   */

  const dispatcher = createEventDispatcher();
  /**
   * @param {import("src/relay_types/flow").DataTransfer}
   * */
  export let flow = {};

  let isMounted = false;

  onMount(function () {
    isMounted = true;
  });
  $: if (browser === true && isMounted === true) {
    createFlowNetwork(flow).then(function () {
      console.log("ok");
    });
  }
  /**
   * @type {FlowController}
   */
  let controller;
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

  export function moveToNode(nodeId) {
    controller.moveToNode(nodeId);
  }

  /**
   *
   * @param {import("src/relay_types/flow").DataTransfer} data
   */
  async function createFlowNetwork(data) {
    controller = await FlowControllerBuilder(container);
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
   * @param {import("./flow").GridInfo} gridInfo
   * @param {MouseEvent} mouseEvent
   */
  function onNodeOver(gridInfo, mouseEvent) {
    /**
     * @type {EventMessage}
     *
     * */
    const message = { gridInfo, mouseEvent };
    tooltipMessage = `${gridInfo.nodes[0].title.slice(0, 10)}…`;
    if (gridInfo.isOverwraped) {
      tooltipMessage += ` + ${gridInfo.nodes.length - 1} articles`;
    }
    toolTip.show(mouseEvent.clientY, mouseEvent.screenX, tooltipMessage);

    dispatcher("NodeOver", message);
  }
  /**
   *
   * @param {import("./flow").GridInfo} gridInfo
   * @param {MouseEvent} mouseEvent
   */
  function onNodeOverOut(gridInfo, mouseEvent) {
    toolTip.hide();
    /**
     * @type {EventMessage}
     *
     * */
    const message = { gridInfo, mouseEvent };
    dispatcher("NodeOverOut", message);
  }
  /**
   * @type {NodeModal}
   */
  let nodeModal;
  /**
   * @param {import("./flow").GridInfo} gridInfo
   * @param {MouseEvent} mouseEvent
   */
  function onNodeClick(gridInfo, mouseEvent) {
    nodeModal.open(gridInfo);
    toolTip.hide();
  }
  // gurd function for prpagation to body
  function voidFunc() {}
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="container root" bind:this={containerRoot}>
  <div class="container" bind:this={container} />

  <NodeModal bind:this={nodeModal} />
</div>
<Tooltip bind:this={toolTip} flowElement={containerRoot} />

<style>
  .root {
    position: relative;
    top: 0%;
    left: 0%;
  }
  .container {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: white;
  }
</style>
