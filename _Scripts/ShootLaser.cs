using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ShootLaser : MonoBehaviour {

    public List<GameObject> lasers;
    public GameObject laserbeamPrefab;
    int nextUpdate = 10;

    // Use this for initialization
    void Start () {
        lasers = new List<GameObject>();
        nextUpdate = Random.Range(10, 15);
	}
	
	// Update is called once per frame
	void Update () {

        if (Time.time >= nextUpdate)
        {
            nextUpdate = Mathf.FloorToInt(Time.time) + Random.Range(6, 10);

            SpawnLaserbeam();
        }
    }

    void SpawnLaserbeam()
    {
        GameObject go = lasers.Find(g => !g.activeSelf);


        if (go == null)
        {
            go = Instantiate(laserbeamPrefab, transform.position, Quaternion.identity);
            go.GetComponent<Laserbeam>().origin = gameObject;
            lasers.Add(go);
        }
        else
        {
            go.transform.position = transform.position;
            go.SetActive(true);
        }

        
    }
}
