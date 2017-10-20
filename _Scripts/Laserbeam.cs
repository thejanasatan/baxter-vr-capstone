using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Laserbeam : MonoBehaviour {

    [SerializeField] GameObject player;
    public GameObject origin;
    [SerializeField] Vector3 target;
    //float speed = 150f;
    float speed = 150f;
    bool isReflected;

	// Use this for initialization
	void Start () {
        
    }
	
	// Update is called once per frame
	void Update () {

	}

    private void OnEnable()
    {
        player = GameObject.FindGameObjectWithTag("MainCamera");

        if (player == null)
            return;

        gameObject.GetComponent<Rigidbody>().velocity = Vector3.zero;

        target = player.transform.position;
        gameObject.transform.LookAt(target);

        //LaunchProjectile(player.transform.position);
        gameObject.GetComponent<Rigidbody>().AddForce(transform.forward * speed);

        DisableSelf();
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Lightsaber")
        {
            //gameObject.SetActive(false);
            //LaunchProjectile(gameObject.transform.position);
            gameObject.GetComponent<Rigidbody>().velocity = Vector3.zero;
            target = origin.transform.position;
            gameObject.transform.LookAt(target);
            gameObject.GetComponent<Rigidbody>().AddForce(transform.forward * speed);
            isReflected = true;
        }

        if (other.tag == "MainCamera")
        {
            gameObject.SetActive(false);
        }

        if (other.tag == "Shooter")
        {
            if (isReflected)
            {
                other.gameObject.SetActive(false);
                gameObject.SetActive(false);
            }
        }
    }

    void LaunchProjectile(Vector3 pos)
    {
        target = pos;
        gameObject.transform.LookAt(target);
    }

    IEnumerator DisableSelf()
    {
        yield return new WaitForSeconds(15);
        gameObject.SetActive(false);
    }
}
