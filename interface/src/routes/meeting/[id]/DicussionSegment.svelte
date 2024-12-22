<script>
  import Section from "$lib/elements/GuiComponent/Section.svelte";
  import SpeechLink from "$lib/url/kokkai/SpeechLink.svelte";

  import { ListGroup, ListGroupItem } from "@sveltestrap/sveltestrap";
  /**
   * @type {import("$lib/ml_api/api_types/MeetingData").Discussion}
   */
  export let discussion;
</script>

<Section>
  <h3 class="section_header fs-5">{discussion.speaker.name}</h3>
  <ListGroup>
    {#each discussion.speeches as speech}
      <ListGroupItem>
        <SpeechLink id={speech.id}>{speech.title}</SpeechLink>
      </ListGroupItem>
    {/each}
  </ListGroup>
</Section>
