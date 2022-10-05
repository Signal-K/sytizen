package main

import (
	"container/list"

	"github.com/charmbracelet/bubbles/list"
)

type status int

const (
	todo status = iota
	inProgress
	done
)

// Custom Item
type Task struct {
	status      status
	title       string
	description string
}

// Implement list.Item interface
func (t Task) FilterValue() string {
	return t.tile
}

func (t Task) Title() string {
	return t.tile
}

func (t Task) Description() string {
	return t.description
}

// Main model
type Model struct {
	list list.Model
	err  error
}

func (m *Model) initList() {
	m.list = list.New([]list.Item{}, list.NewDefaultDelegate())
}
