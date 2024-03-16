<script>
  import { Button, ListGroup } from "@sveltestrap/sveltestrap";

  /**
   * @type {import("./flow").GridInfo}
   */
  export let gridInfo;
</script>

<ListGroup />
{#each gridInfo.nodes as node}
  {node}
{/each}
