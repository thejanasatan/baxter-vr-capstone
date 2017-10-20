using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Lightsaber : MonoBehaviour {
    public GameManager gameManager;

    public AudioClip clipHum;
    public AudioClip clipClash;

    private AudioSource audioHum;
    private AudioSource audioClash;

    [SerializeField]
    private UDPSend UDPScript;
    public GameObject baxter;

    public bool isPlayerController;

    //public GameObject baxter;
    //public BaxterController baxterController;

    public GameObject lensFlarePrefab;
    public GameObject lensFlare;

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
        //gameManager = GameManager.Instance;'

        if (baxter == null)
            baxter = GameObject.FindGameObjectWithTag("Network");
        UDPScript = baxter.GetComponent<UDPSend>();


        lensFlare = Instantiate(lensFlarePrefab, gameObject.transform);
        lensFlare.SetActive(false);

    }

    private void Start()
    {
        audioHum.Play();
        //if (gameObject.GetComponent<LightsaberTracker>() == null)
        //{
        //    isPlayerController = false;
        //} else
        //{
        //    isPlayerController = true;
        //}
        if (isPlayerController)
        {
            Renderer laser = gameObject.GetComponent<Renderer>();
            //change lightsaber colourto blue if player
            laser.material.color = Color.blue;
        }
    }

    private void OnCollisionEnter(Collision collision)
    {
        if (isPlayerController /*|| gameManager.inCinematicMode*/)
        {
            return;
        }

        if (collision.gameObject.tag == "Lightsaber" || collision.gameObject.tag == "MainCamera")
        {
            //Debug.Log("Clash!");
            audioClash.Play();
            UDPScript.sendString("clash");
            //UDPScript.sendString("clash");
            //UDPScript.sendString(Random.Range(1, 4).ToString());
            //baxter.GetComponent<BaxterController>().SendBaxterMessage(0);
            //baxterController.SendBaxterMessage(Random.Range(0, 3));
        }
        else
        {
            audioClash.Stop();
        }
    }

    private void OnCollisionStay(Collision collision)
    {
        //print("Flare");
        //ContactPoint contact = collision.contacts[0];
        ////Quaternion rot = Quaternion.FromToRotation(Vector3.up, contact.normal);
        //Vector3 pos = contact.point;
        //lensFlare.transform.position = pos;
        //lensFlare.SetActive(true);
        if (collision.gameObject.tag == "Lightsaber")
        {
            //if (!gameManager.isRunning)
            //{
            //	return;
            //}
            //print("Flare");
            ContactPoint contact = collision.contacts[0];
            //Quaternion rot = Quaternion.FromToRotation(Vector3.up, contact.normal);
            Vector3 pos = contact.point;
            lensFlare.transform.position = pos;
            lensFlare.SetActive(true);
        }
        //else
        //{
        //    //print("No Flare");
        //    //lensFlare.SetActive(false);
        //}
    }

    private void OnCollisionExit(Collision collision)
    {
        if (collision.gameObject.tag == "Lightsaber")
        {
            //print("No Flare");
            lensFlare.SetActive(false);
        }
    }

    //private void OnTriggerEnter(Collider other)
    //{
    //    if (isPlayerController)
    //    {
    //        return;
    //    }

    //    if (other.gameObject.tag == "Lightsaber" || other.gameObject.tag == "MainCamera")
    //    {
    //        Debug.Log("Clash!");
    //        audioClash.Play();
    //        //UDPScript.sendString("Clash");
    //        UDPScript.sendString(Random.Range(1, 4).ToString());
    //    }
    //    else
    //    {
    //        audioClash.Stop();
    //    }
    //}

}
