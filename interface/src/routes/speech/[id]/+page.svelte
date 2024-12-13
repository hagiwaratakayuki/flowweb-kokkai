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
            <span>{data.speaker.name}</span>
            {#if checkAdditionalData()}
              (
              {#each getAdditionalData() as additionalData}
                <span class="pr-2">{additionalData}</span>
              {/each}
              )
            {/if}
          </dd>
          <dt>委員会</dt>
          <dd>
            <span class="pr-2">第{data.speech.session}回</span>
            <span class="pr-2">{data.speech.house}</span>
            <span class="pr-2">{data.speech.meeting}</span>
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
        <ListGroup flush={true}>
          {#each data.clusters.overviews as cluster}
            <ListGroupItem>
              <KokkaiFlowLink id={cluster.id} keywords={cluster.keywords} />
            </ListGroupItem>
          {/each}
        </ListGroup>
      </Panel>
    </Section>
    <h2 class="section_header">他の発言との繋がり</h2>
    <Section>
      <Row>
        <Col md="6">
          <h3 class="section_header">この発言に繋がる発言</h3>
          <Panel>
            <ListGroup flush={true}>
              {#each data.link_from.nodes as node}
                <ListGroupItem>
                  <SpeechLink id="{node.id}}">{node.title}</SpeechLink>
                </ListGroupItem>
              {/each}
            </ListGroup>
          </Panel>
        </Col>
        <Col md="6">
          <h3 class="section_header">この発言から繋がる発言</h3>
          <Panel>
            <ListGroup flush={true}>
              {#each data.link_to as link}
                <ListGroupItem>
                  <SpeechLink id={link.id}>{link.title}</SpeechLink>
                </ListGroupItem>
              {/each}
            </ListGroup>
          </Panel>
        </Col>
      </Row>
    </Section>
  </Col>
</Row>
