<script>
  import Section from "$lib/elements/GuiComponent/Section.svelte";
  import ListItem from "$lib/elements/TextOverview/ListItem.svelte";
  import SpeakerLink from "$lib/url/kokkai/SpeakerLink.svelte";
  import { ListGroup } from "@sveltestrap/sveltestrap";

  /**
   * @type
   */
  export let houseAndSpeaker;

  let house;
  /** 
    
    * @type {import("$lib/ml_api/api_types/SpeakerData").SpeakerSingle[]} 
    
    */
  let speakers;
  $: {
    house = houseAndSpeaker[0];
    speakers = houseAndSpeaker[1];
  }
</script>

<h3 class="section_header fs-5">{house}</h3>
<Section>
  <ListGroup class="bg-white">
    {#each speakers as speaker}
      <ListItem>
        <SpeakerLink id={speaker.id}>
          <span class="pr-2">第{speaker.session}回</span>
          <span class="pr-2">{speaker.comittie}</span>
          {#if speaker.group}
            <span class="pr-2">{speaker.group}</span>
          {/if}
          {#if speaker.position}
            <span class="pr-2">{speaker.position}</span>
          {/if}
          {#if speaker.role}
            <span class="pr-2">{speaker.role}</span>
          {/if}
        </SpeakerLink>
      </ListItem>
    {/each}
  </ListGroup>
</Section>
