package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/eclipse-fog05/api-go/fog05"
	"github.com/eclipse-fog05/sdk-go/fog05sdk"
)

func check(e error) {
	if e != nil {
		panic(e)
	}

}

const n1 = "4a560914-1c3e-4966-9fa8-7f0acc903253" //nuc

// const n1 = "53712df2-9649-4a21-be2e-80eed00ff9ce" //ubuntuvm1local

func main() {
	args := os.Args[1:]
	api, err := fog05.NewFIMAPI(args[0], nil, nil)
	check(err)

	fmt.Printf("Nodes:\n")
	nodes, err := api.Node.List()
	check(err)

	for _, n := range nodes {
		fmt.Printf("UUID: %s\n", n)
	}

	data, err := ioutil.ReadFile(args[1])
	check(err)

	var fduDescriptor fog05sdk.FDU
	json.Unmarshal(data, &fduDescriptor)

	data, err = ioutil.ReadFile(args[2])
	check(err)

	var vNetDescriptor fog05sdk.VirtualNetwork
	json.Unmarshal(data, &vNetDescriptor)

	fmt.Printf("Press enter to create network\n")
	bufio.NewReader(os.Stdin).ReadBytes('\n')

	err = api.Network.AddNetwork(vNetDescriptor)
	check(err)
	vNetR, err := api.Network.AddNetworkToNode(n1, vNetDescriptor)
	check(err)

	fmt.Printf("Result of Network creation\n%+v\n", vNetR)

	fmt.Printf("Press enter to onboard descriptor\n")
	bufio.NewReader(os.Stdin).ReadBytes('\n')
	// time.Sleep(5 * time.Second)

	fduD, err := api.FDU.Onboard(fduDescriptor)
	check(err)
	fmt.Printf("Result of onboarding\n%+v\n", fduD)

	fID := *fduD.UUID

	fmt.Printf("Press enter to define\n")
	bufio.NewReader(os.Stdin).ReadBytes('\n')

	// time.Sleep(5 * time.Second)

	fduR, err := api.FDU.Define(n1, fID)
	check(err)
	fmt.Printf("Result of define:\n%+v\n", fduR)

	iID := fduR.UUID

	fmt.Printf("Press enter to configure\n")
	bufio.NewReader(os.Stdin).ReadBytes('\n')
	// time.Sleep(30 * time.Second)
	_, err = api.FDU.Configure(iID)
	check(err)

	fmt.Printf("Press enter to start\n")
	bufio.NewReader(os.Stdin).ReadBytes('\n')
	// time.Sleep(30 * time.Second)
	_, err = api.FDU.Start(iID)
	check(err)

	fmt.Printf("Press enter to get instance info\n")
	bufio.NewReader(os.Stdin).ReadBytes('\n')
	// time.Sleep(30 * time.Second)
	info, err := api.FDU.InstanceInfo(iID)
	check(err)

	fmt.Printf("Instance Info:\n%+v\n", info)

	fmt.Printf("Press enter to stop\n")
	bufio.NewReader(os.Stdin).ReadBytes('\n')
	// time.Sleep(30 * time.Second)
	_, err = api.FDU.Stop(iID)
	check(err)

	fmt.Printf("Press enter to Clean\n")
	bufio.NewReader(os.Stdin).ReadBytes('\n')
	// time.Sleep(30 * time.Second)
	_, err = api.FDU.Clean(iID)
	check(err)

	fmt.Printf("Press enter to Remove\n")
	bufio.NewReader(os.Stdin).ReadBytes('\n')
	// time.Sleep(30 * time.Second)
	_, err = api.FDU.Undefine(iID)
	check(err)

	_, err = api.FDU.Offload(fID)
	check(err)

	fmt.Printf("Press enter to Remove Network\n")
	bufio.NewReader(os.Stdin).ReadBytes('\n')

	_, err = api.Network.RemoveNetworkFromNode(n1, vNetR.UUID)
	check(err)
	err = api.Network.RemoveNetwork(vNetR.UUID)
	check(err)

}
