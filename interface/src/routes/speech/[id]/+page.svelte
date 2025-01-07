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
  import MeetingLink from "$lib/url/kokkai/MeetingLink.svelte";
  import SpeakerLink from "$lib/url/kokkai/SpeakerLink.svelte";
  import HtmlHeader from "$lib/elements/HtmlHeader.svelte";

  /** @type {import('./$types').PageData} */
  export let data;

  /**
   * @type {HTMLElement}
   */
  let linkTo;
  /**
   * @type {HTMLElement}
   */
  let linkedFrom;

  function scrollLinkTo() {
    linkTo.scrollIntoView({ behavior: "smooth" });
  }
  function scrollLinkedFrom() {
    linkedFrom.scrollIntoView({ behavior: "smooth" });
  }
  /**
   *
   * @param {string} text
   */
  function splitbr(text) {
    return text.split(/(\r|\n|\r\n)/);
  }

  function checkAdditionalData() {
    return (
      !!data.speaker.group || !!data.speaker.position || !!data.speaker.role
    );
  }
  /**
   *
   * @param {Element}elm
   * @param isActive
   */
  function scrollDiscussion(elm, isActive) {
    if (isActive == true) {
      elm.scrollIntoView({ behavior: "smooth" });
    }
    if (typeof Window != "undefined") {
      window.scroll(0, 0);
    }
  }
  // @todo 区切り線判定(前に要素があるか)追加。groupにはリンクつける
  function getAdditionalData() {
    return [
      data.speaker.group,
      data.speaker.position,
      data.speaker.role,
    ].filter(function (r) {
      return !!r;
    });
  }
</script>

<HtmlHeader
  title={"第" +
    data.speech.session +
    "回" +
    data.speech.house +
    data.speech.meeting +
    "第" +
    data.speech.issue +
    "号 発言番号" +
    data.speech.order +
    "(" +
    data.speaker.name +
    ")"}
></HtmlHeader>
<Row class="justify-content-md-center">
  <Col md="2" sm="12" class="sticky">
    <h2 class="section_header">質疑</h2>
    <div class="h-80vh">
      <div class="vertical-scroll">
        <ul class="list-group bg-white">
          {#each data.discussion as discussion}
            <li
              class="list-group-item"
              class:active={discussion.id === data.speech.id}
              aria-current={discussion.id === data.speech.id}
              use:scrollDiscussion={discussion.id === data.speech.id}
            >
              {#if discussion.id !== data.speech.id}
                <SpeechLink id={discussion.id}>{discussion.title}</SpeechLink>
              {:else}
                {discussion.title}
              {/if}
            </li>
          {/each}
        </ul>
      </div>
    </div>
  </Col>
  <Col md="10" sm="12">
    <Section>
      <h2 class="section_header">キーワード</h2>
      <Panel>
        {#each keywordPretter(data.keywords) as keyword}
          <span>{keyword} </span>
        {:else}
          <span>キーワードはありません</span>
        {/each}
      </Panel>
    </Section>
    <h2 class="section_header">発言</h2>
    <Section>
      <Panel>
        {#each splitbr(data.speech.body) as line}
          {line}<br />
        {/each}
      </Panel>
      <Panel>
        <dl>
          <dt>発言者</dt>
          <dd>
            <SpeakerLink id={data.speaker.id}>{data.speaker.name}</SpeakerLink>
            {#if checkAdditionalData()}
              (
              {#each getAdditionalData() as additionalData}
                <span class="pe-2">{additionalData}</span>
              {/each}
              )
            {/if}
          </dd>
          <dt>委員会</dt>
          <dd>
            <span class="pe-2">第{data.speech.session}回</span>
            <span class="pe-2">{data.speech.house}</span>
            <span class="pe-2">
              <MeetingLink id={data.speech.meeting_id}>
                {data.speech.meeting}
              </MeetingLink>
            </span>
            <span>第{data.speech.issue}号</span>
          </dd>
        </dl>
        <p>
          <a href={data.speech.url} target="_blank">この発言を会議録で見る</a>
        </p>
      </Panel>
    </Section>
    <h2 class="section_header">この発言を含む議論</h2>
    <Section>
      <Panel>
        {#if (data.clusters || []).length !== 0}
          <ListGroup flush={true}>
            {#each data.clusters?.overviews || [] as cluster}
              <ListGroupItem>
                <KokkaiFlowLink id={cluster.id} keywords={cluster.keywords} />
              </ListGroupItem>
            {/each}
          </ListGroup>
        {:else}
          <span>この発言を含む議論はありません</span>
        {/if}
      </Panel>
    </Section>
    <h2 class="section_header">他の発言との繋がり</h2>
    <Section>
      <Row>
        <Col md="6">
          <h3 class="section_header">この発言に繋がる発言</h3>

          <Panel>
            {#if (data.link_from?.nodes || []).length !== 0}
              <ListGroup flush={true}>
                {#each data.link_from?.nodes || [] as node}
                  <ListGroupItem>
                    <SpeechLink id="{node.id}}">{node.title}</SpeechLink>
                  </ListGroupItem>
                {/each}
              </ListGroup>
            {:else}
              <span>この発言に繋がる発言はありません</span>
            {/if}</Panel
          >
        </Col>
        <Col md="6">
          <h3 class="section_header">この発言から繋がる発言</h3>
          <Panel>
            {#if (data.link_to || []).length !== 0}
              <ListGroup flush={true}>
                {#each data.link_to || [] as link}
                  <ListGroupItem>
                    <SpeechLink id={link.id}>{link.title}</SpeechLink>
                  </ListGroupItem>
                {/each}
              </ListGroup>
            {:else}
              <span>この発言から繋がる発言はありません</span>
            {/if}
          </Panel>
        </Col>
      </Row>
    </Section>
  </Col>
</Row>
