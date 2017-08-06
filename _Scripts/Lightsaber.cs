using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Lightsaber : MonoBehaviour {

    public AudioClip clipHum;
    public AudioClip clipClash;

    private AudioSource audioHum;
    private AudioSource audioClash;

    public AudioSource AddAudio(AudioClip clip, bool loop, bool playAwake, float vol)
    {
        AudioSource newAudio = gameObject.AddComponent<AudioSource>();

        newAudio.clip = clip;
        newAudio.loop = loop;
        newAudio.playOnAwake = playAwake;
        newAudio.volume = vol;

        return newAudio;
    }

    private void Awake()
    {
        audioHum = AddAudio(clipHum, true, false, 0.5f);
        audioClash = AddAudio(clipClash, false, false, 0.5f);
    }

    private void Start()
    {
        audioHum.Play();
    }

    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.tag == "Lightsaber")
        {
            Debug.Log("Clash!");
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.tag == "Lightsaber")
        {
            Debug.Log("Clash!");
            audioClash.Play();
        } else
        {
            audioClash.Stop();
        }
    }
}
