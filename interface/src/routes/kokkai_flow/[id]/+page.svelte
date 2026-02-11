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
  import { keywordPretter } from "$lib/util/keyword_pretter";
  import HtmlHeader from "$lib/elements/HtmlHeader.svelte";
  /** @type {import('./$types').PageData} */
  export let data;

  let links = data.flow.links || [];
</script>

<HtmlHeader
  title={keywordPretter(data.flow.keywords).join(" ") +
    "についての議論(第" +
    data.flow.session +
    "回国会)"}
></HtmlHeader>
<FlowWithTextList data={data.flow.members.nodes}>
  <div slot="sidebar" class="void">
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
  <div slot="main" class="void">
    <h2 class="section_header">キーワード</h2>
    <Section>
      <Panel>
        {#each keywordPretter(data.flow.keywords) as keyword}
          <span class="pe-2">{keyword}</span>
        {/each}
      </Panel>
    </Section>
    <Section>
      <Panel>
        <dl>
          <dt>回次</dt>
          <dd>第{data.flow.session}回</dd>
          <dt>発言数</dt>
          <dd>{data.flow.member_count}</dd>
        </dl>
      </Panel>
    </Section>
    <Section>
      <Panel>
        <div class="text-center">
          {#if data.flow.before_cluster}
            <KokkaiFlowLink id={data.flow.before_cluster.id}
              >&lt; 以前の議論(第{data.flow.before_cluster
                .session}回)</KokkaiFlowLink
            >
          {:else}
            <span class="text-black-50" aria-disabled="true"
              >&lt; 以前の議論</span
            >
          {/if}
          <span class="px-2">|</span>
          {#if data.flow.before_cluster}
            <KokkaiFlowLink id={data.flow.after_cluster.id}
              >次の議論(第{data.flow.after_cluster.session}回) &gt;</KokkaiFlowLink
            >
          {:else}
            <span class="text-black-50" aria-disabled="true">次の議論 &gt;</span
            >
          {/if}
        </div>
      </Panel>
    </Section>
  </div>
</FlowWithTextList>
