<script>
  import { tick } from "svelte";
  import { ListGroup, ListGroupItem } from "@sveltestrap/sveltestrap";

  /**
   * @typef {import("./flow").GridInfo} GridInfo
   * @type {GridInfo}
   */
  let _interactiveData = { nodes: [], isOverwraped: false };

  let isVisible = false;

  let frameHeight = 0;
  let contentHeight = 0;
  let isScroll = false;
  let lock = true;

  $: {
    isScroll = frameHeight < contentHeight;
  }
  export function close() {
    isVisible = false;
  }
  export function open(interactiveData) {
    isVisible = true;
    lock = true;
    isScroll = false;
    _interactiveData = interactiveData;
  }
  function bodyClick() {
    setTimeout(function () {
      if (lock === true) {
        lock = false;
        return;
      }
      close();
    });
  }
</script>

{#if isVisible === true}
  <div
    class="frame w-80 rounded-1 bg-light"
    class:vertical-scroll={isScroll}
    bind:clientHeight={frameHeight}
  >
    <div bind:clientHeight={contentHeight} class="px-4 pb-4 pt-1 content">
      <div class="mb-2 text-end">
        <button
          type="button"
          class="btn-close close"
          aria-label="Close"
          on:click={close}
        />
      </div>
      <ListGroup class="bg-white rounded-2">
        {#each _interactiveData.nodes as node}
          <ListGroupItem>
            <a href="/text/{node.id}">{node.title}</a>
          </ListGroupItem>
        {/each}
      </ListGroup>
    </div>
  </div>
{/if}
<svelte:body on:click={bodyClick} />

<style>
  .frame {
    position: absolute;
    top: 0px;
    left: 20%;
    max-height: 90%;
  }
  .content {
    height: auto;
  }
  .close {
    background-size: 12px;
  }
</style>
