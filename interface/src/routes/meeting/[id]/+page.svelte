<script>
  import {
    Row,
    Col,
    Button,
    ListGroup,
    ListGroupItem,
  } from "@sveltestrap/sveltestrap";
  import { encode } from "html-entities";
  import Panel from "$lib/elements/GuiComponent/Panel.svelte";
  import Section from "$lib/elements/GuiComponent/Section.svelte";
  import { keywordPretter } from "$lib/util/keyword_pretter";
  import KokkaiFlowLink from "$lib/url/kokkai/KokkaiFlowLink.svelte";
  import DicussionSegment from "./DicussionSegment.svelte";
  import HtmlHeader from "$lib/elements/HtmlHeader.svelte";

  /** @type {import('./$types').PageData} */
  export let data; /**
   *
   */
  function getTitle(_data) {
    return [
      "第" + data.session + "回",
      _data.house,
      _data.name,
      "第" + _data.issue + "号",
    ].join("");
  }
</script>

<HtmlHeader title={getTitle(data.data)}></HtmlHeader>
<Row class="justify-content-md-center">
  <Col md="2" sm="12" class="sticky">
    <h2 class="section_header">質疑</h2>
    <div class="h-80vh">
      <div class="vertical-scroll">
        {#each data.discussions as discussion}
          <DicussionSegment {discussion} />
        {/each}
      </div>
    </div>
  </Col>
  <Col md="10" sm="12">
    <h1 class="section_header fs-2">
      <span class="pr-2">第{data.data.session}回</span>
      <span class="pr-2">{data.data.house}</span>
      <span class="pr-2">{data.data.name}</span>
      <span class="pr-2">第{data.data.issue}号</span>
    </h1>

    <Section>
      <Panel>
        <pre>{encode(data.data.header_text)}</pre>
      </Panel>
    </Section>
    <Section>
      <Panel>
        <dl>
          <dt>委員長</dt>
          <dd>
            {#each data.data.moderators as moderator}
              {moderator.name}<br />
            {/each}
          </dd>
          <dt>リンク</dt>
          <dd>
            <a href={data.data.url} target="_blank">会議録</a>
            <a href={data.data.pdf} target="_blank">PDF</a>
          </dd>
        </dl>
      </Panel>
    </Section>
  </Col>
</Row>
