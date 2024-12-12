<script>
  import {
    Row,
    Col,
    Button,
    ListGroup,
    ListGroupItem,
  } from "@sveltestrap/sveltestrap";

  import Panel from "$lib/elements/GuiComponent/Panel.svelte";
  import Section from "$lib/elements/GuiComponent/Section.svelte";
  import SpeechLink from "$lib/url/kokkai/SpeechLink.svelte";
  import FlowWithTextList from "$lib/elements/Kokkai/Flow.svelte";
  import GridLayout from "$lib/elements/GuiComponent/GridLayout.svelte";
  import Flow from "$lib/elements/Flow/Flow.svelte";
  import KokkaiFlowLink from "$lib/url/kokkai/KokkaiFlowLink.svelte";
  /** @type {import('./$types').PageData} */
  export let data;
  let links = data.flow.links;
</script>

<GridLayout>
  <div slot="side">
    <h2 class="section_header">関連する議論</h2>
    <Panel class="h-40vh">
      <div class="vertical-scroll">
        <ListGroup>
          {#each links as link}
            <ListGroupItem>
              <KokkaiFlowLink id={link.id} keywords={link.keywords} />
            </ListGroupItem>
          {/each}
        </ListGroup>
      </div>
    </Panel>
  </div>
  <div slot="main" class="void"></div>
</GridLayout>
<FlowWithTextList data={data.flow.members.nodes}></FlowWithTextList>
