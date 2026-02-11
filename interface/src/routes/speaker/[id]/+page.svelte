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
  import { keywordPretter } from "$lib/util/keyword_pretter";
  import KokkaiFlowLink from "$lib/url/kokkai/KokkaiFlowLink.svelte";
  import HouseAndSpeker from "./HouseAndSpeker.svelte";
  import HtmlHeader from "$lib/elements/HtmlHeader.svelte";

  /** @type {import('./$types').PageData} */
  export let data;
</script>

<HtmlHeader
  title={data.speaker.name +
    "(第" +
    data.speaker.session +
    "回" +
    data.speaker.house +
    data.speaker.comittie +
    ")"}
></HtmlHeader>
<Row class="justify-content-md-center">
  <Col md="2" sm="12" class="sticky">
    <h2 class="section_header">同名の人物</h2>
    {#if data.same_names.length == 0}
      <Panel><p>記録されていません</p></Panel>
    {:else}
      <div class="h-80vh">
        <div class="vertical-scroll">
          <ul class="list-group bg-white">
            {#each data.same_names as houseAndSpeaker}
              <HouseAndSpeker {houseAndSpeaker}></HouseAndSpeker>
            {/each}
          </ul>
        </div>
      </div>
    {/if}
  </Col>
  <Col md="10" sm="12">
    <h1 class="section_header fs-2">
      {data.speaker.name}(第{data.speaker.session}回{data.speaker.house}{data
        .speaker.comittie})
    </h1>
    <Section>
      <Panel>
        <dl>
          {#if data.speaker.group}
            <dt>会派</dt>
            <dd>{data.speaker.group}</dd>
          {/if}
          {#if data.speaker.position}
            <dt>役職</dt>
            <dd>{data.speaker.position}</dd>
          {/if}
          {#if data.speaker.role}
            <dt>役割</dt>
            <dd>{data.speaker.role}</dd>
          {/if}
        </dl>
      </Panel>
    </Section>
    <h2>発言</h2>
    <ListGroup>
      {#each data.speeches as speech}
        <ListGroupItem>
          <SpeechLink id={speech.id}>{speech.title}...</SpeechLink>
        </ListGroupItem>
      {/each}
    </ListGroup>
  </Col>
</Row>
